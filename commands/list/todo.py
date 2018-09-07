from graph import GraphItem
from due import *

class Todo(GraphItem):
    def __init__(self, summary, level, type, due, references, filename, has_keyword, line_number):
        GraphItem.__init__(self)
        self.summary = summary
        self.level = level
        self.type = type
        self.due = due
        self.references = references
        self.filename = filename
        self.has_keyword = has_keyword
        self.line_number = line_number
        self.done = False

    def getSummary(self):
        return self.name

    def setSummary(self, name):
        self.name = name

    def getDue(self):
        if self.due is None:
            return Due()
        return self.due

    def setDue(self, due):
        self.due = due

    def getReferences(self):
        return set(self.references)

    def match(self, key):
        key = key.lower()
        keys = key.split('/')
        names = []
        p = self
        while p.parent:
            p = p.parent
            names.append(p.summary.lower())
        names = [x for x in reversed(names)]
        for j,k in enumerate(keys[:-1]):
            k_match = False
            for i,n in enumerate(names):
                if n.startswith(k):
                    names = names[i+1:]
                    k_match = True
                    break
            if not k_match:
                return False
        return self.summary.startswith(keys[-1])

    def count(self):
        total = 0
        for child in self.children:
            total += child.count()
        self_total = 1 if self.is_today() and self.has_keyword else 0
        return max(total, self_total)

    def __repr__(self):
        return self.string()
        return '{:15} {:2} {:6} {:15} {:25}'.format(self.summary,
                                                         self.level,
                                                         self.type,
                                                         self.due,
                                                         self.references)

    def string(self, lite=True, table=False):
        start = ''
        if not lite:
            if self.level >= 7:
                start = ' '*(self.level-7)
            else:
                start = '#'*(self.level-1)
            if self.type:
                start += str(self.type)
                if isinstance(self.type, int):
                    start += '.'
                start += ' '

        else:
            start = '  '*self.depth()
            if isinstance(self.type, int):
                start += str(self.type)+'. '

        summary = self.summary
        if table:
            summary = summary.replace(' ', '_')
        s = start+summary
        if isinstance(self.due, DueDate) or isinstance(self.due, DueWeekly):
            s += ' @{}'.format(self.due)
        if self.references:
            s += ' [{}]'.format(', '.join(self.references))
        return s

    def is_overdue(self):
        return self.due.days_until() < 0

    def is_today(self):
        return self._is_today() and not self.is_soon()

    def _is_today(self):
        if self.is_comment():
            return False
        if self.are_dependers_today() and not self.is_blocked():
            return True
        if isinstance(self.due, DueDate) or isinstance(self.due, DueWeekly):
            return self.due.is_today()
        return False # not self.is_blocked()

    def is_soon(self):
        if self.is_comment():
            return False
        if self.are_dependers_today() and not self.is_blocked():
            return False
        if self.are_dependers_soon() and not self.is_blocked():
            return True
        if self.is_blocked() and self._is_today():
            return True
        if self.due.days_until() == Due.Never:
            return not self.is_blocked()
        return False

    def are_dependers_today(self):
        for d in self.dependers:
            if d._is_today() or d.are_dependers_today():
                return True
        if self.parent:
            return self.parent.are_dependers_today()
        return False

    def are_dependers_soon(self):
        for d in self.dependers:
            if d.is_soon() or d.are_dependers_soon():
                return True
        if self.parent:
            return self.parent.are_dependers_soon()
        return False


    def get_blocking_relatives(self):
        rel = filter(lambda x: x.has_keyword or
                     x.get_blocking_relatives(), self.children)
        return rel

    def is_blocked(self):
        if self.get_blocking_relatives():
            return True
        for d in self.dependencies:
            if d.is_blocking():
                return True
        return False

    def is_blocking(self):
        if isinstance(self.due, DueWeekly):
            return False
        return True

    def is_comment(self):
        return self.type == ''

    def is_filename(self):
        return self.type == 'file'

    def has_keyword_child(self):
        for c in self.get_children():
            if c.has_keyword  or c.has_keyword_child():
                return True
        return False


    def full_name(self):
        s = self.summary
        if self.parent:
            s = self.parent.full_name() + '/' + s
        return s

    # def remove(self):
    #     self.due = Due()
    #     self.mark_done()
    # def is_done(self):
    #     return self.done
    #
    # def mark_done(self):
    #     if isinstance(self.due, DueWeekly):
    #         self.due.next_due()
    #     else:
    #         self.done = True
    #
    #
    # def __lt__(self, other):
    #     return self.string() < other.string()
