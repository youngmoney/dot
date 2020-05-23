from graph import *
from due import *
from todo import *

try:
    if DEBUG:
        pass
except:
    DEBUG = False

class TodoList:
    def __init__(self, file_iter):
        items = self.parse(file_iter)
        self.graph = self.connect(items)

    def string(self, **kwargs):
        return '\n'.join(self._string(**kwargs))

    def table(self, **kwargs):
        return '\n'.join(self._table(**kwargs))

    def _string(self, lite=True, color=True, graph=None):
        for i in self.graph.iterate():
            if lite and not i.has_keyword and not i.has_keyword_child():
                continue
            if lite and i.is_comment():
                continue
            c = ''
            if i.is_overdue():
                c = Pretty.red
            elif i.is_today():
                c = Pretty.blue
            elif i.is_soon():
                c =  Pretty.green + Pretty.bold
            else:
                c = Pretty.gray
            if not color:
                c = ''

            yield c+ i.string(lite=lite) + Pretty.reset

    def _table(self):
        for i in self.graph.iterate():
            if i.has_keyword:
                yield '"%s" %s: %s (%s)' % (
                        i.filename,
                        i.line_number,
                        i.summary,
                        i.full_name()
                    )

    def count(self):
        count = 0
        # for i in self.graph.iterate():
        #     if i.has_keyword:
        #         count += 1
        for i in self.graph.get_children():
            count += i.count()
        return count

    def tags(self):
        items = []
        for i in self.graph.iterate():
            if i.has_keyword or i.has_keyword_child():
                items.append('%s\t%s\t/%s/' % (
                        i.summary.replace(' ', '_'),
                        i.filename,
                        i.summary,
                    ))
        return '\n'.join(sorted(items))

    @classmethod
    def cleanup_markdown(cls, lines):
        prev = None
        for line in lines:
            chars = set(line)
            if prev is not None and len(chars) == 1:
                if '=' in chars:
                    prev = '# ' + prev
                    line = None
                if '-' in chars:
                    prev = '## ' + prev
                    line = None
            if prev is not None:
                yield prev
            prev = line
        if prev is not None:
            yield prev

    @classmethod
    def line_level_and_type_and_summary(cls, line):
        summary = line.lstrip()
        stripped = summary

        has_keyword = False
        KEYS = ['TODO', 'ACTIONITEM', ' ^ ']

        for k in KEYS:
            if k.lower() in line:
                has_keyword = True
                keep = []
                found = False
                kw = k.strip().lower()
                for w in summary.split(' '):
                    if found or not w.startswith(kw):
                        keep.append(w)
                    else:
                        found = True
                summary = ' '.join(keep)
        level = 7 + len(line) - len(stripped)
        type = '' if not has_keyword else 'action'
        if len(summary) == 0:
            summary = line
            level = -1
            type = None
        elif line.startswith('#'):
            split = summary.split(' ')
            hashes = split[0]
            if len(set(hashes)) == 1:
                summary = ' '.join(split[1:])
                level = len(hashes)
                type = '#'
        elif summary.startswith('-'):
            split = summary.split('- ')
            type = '-'
            summary = '- '.join(split[1:])
        elif summary.startswith('+'):
            split = summary.split('+ ')
            type = '+'
            summary = '+ '.join(split[1:])
        else:
            try:
                i = int(summary.split('.')[0])
                split = summary.split(str(i)+'. ')
                type = i
                summary = (str(i)+'. ').join(split[1:])
            except:
                pass

        return level, type, summary, has_keyword

    @classmethod
    def due_date_and_summary(cls, line):
        parts = []
        due = ''
        for p in line.split(' '):
            if p.startswith('@'):
                due = p[1:]
            else:
                parts.append(p)
        return due, ' '.join(parts)

    @classmethod
    def dependencies_and_summary(cls, line):
        letters = ''
        dependency_letters = ''
        depend = False
        for l in line:
            if l == ']':
                depened = False
            elif l == '[':
                depend = True
            elif depend:
                dependency_letters += l
            else:
                letters += l

        deps = [x.strip() for x in dependency_letters.split(',')]
        deps = [x for x in deps if len(x) > 0]
        return deps, letters


    def parse(self, file_iter):
        items = []
        for filename, lines in file_iter:
            items.append(Todo(filename, 0, 'file', Due(), [], filename, has_keyword=False, line_number=0))
            line_number = 0
            for line in TodoList.cleanup_markdown(lines()):
                line_number += 1
                if line_number > 2500:
                    break
                line = line.rstrip('\n').lower()
                level, type, summary, has_keyword = TodoList.line_level_and_type_and_summary(line)
                due, summary = TodoList.due_date_and_summary(summary)
                dependencies, summary = TodoList.dependencies_and_summary(summary)
                if DEBUG:
                    print('{:30} {:15} {:2} {:6} {:15} {:25}'.format(line, summary, level, type, due, dependencies))

                due = Due.str2due(due)
                if not summary or type is None:
                    continue
                item = Todo(summary, level, type, due, dependencies, filename=filename, has_keyword=has_keyword, line_number=line_number)
                items.append(item)

        return items

    def link(self, items):
        prev = None
        for item in items:
            if prev is not None:
                prev.set_next(item)
            prev = item

    def parent(self, items):
        top = []
        parents = []
        for item in items:
            while parents and parents[-1].level >= item.level:
                parents = parents[:-1]
            if parents:
                parents[-1].add_child(item)
            else:
                top.append(item)

            parents.append(item)

        changed = True
        while changed:
            changed = False
            for item in items:
                children = list(item.get_children())
                if item.is_comment() and children:
                    changed = True
                    item.remove_children(children)
                    if item.parent:
                        item.parent.add_children(children)
                    else:
                        top.append(children)


        return Graph(top)

    def depend(self, graph):
        for item in graph.iterate():
            if item.type == '+':
                parent = item.parent if item.parent else graph.top
                index = parent.children.index(item)
                match = None
                while match is None or match.is_comment() and index > 0:
                    index -= 1
                    match = parent.children[index]
                if index >= 0 and not match.is_comment():
                    item.add_dependency(match)
                    match.add_depender(item)
                    if DEBUG:
                        print('autosetting', item.summary, '->', match.summary)
            for ref in item.getReferences():
                swap = False
                if len(ref) > 0 and ref[0] == '!':
                    ref = ref[1:]
                    swap = True
                matches = self.search(ref, graph)
                if len(matches) == 1:
                    match = list(matches)[0]
                    orig = item
                    if swap:
                        orig, match = match, orig
                    if DEBUG:
                        print('setting', item.summary, '->', match.summary)
                    orig.add_dependency(match)
                    match.add_depender(orig)
                else:
                    pass


    def connect(self, items):
        self.link(items)
        graph = self.parent(items)
        self.depend(graph)
        return graph

    def search(self, key, graph=None):
        if graph is None:
            graph = self.graph
        matches = set()
        for item in graph.iterate():
            if item.match(key):
                matches.add(item)

        return matches

class Pretty:
    reset='\033[0m'
    bold='\033[01m'

    blue='\033[34m'

    red='\033[31m'
    purple='\033[35m'
    yellow='\033[33m'

    green = '\033[32m'
    lightgreen='\033[92m'
    lightblue='\033[94m'
    cyan='\033[36m'
    lightcyan='\033[96m'

    gray='\033[90m'
