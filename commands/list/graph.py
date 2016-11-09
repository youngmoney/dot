class Graph:
    def __init__(self, children=None):
        self.children = []
        self.add_children(children)

    def get_children(self):
        for child in self.children:
            yield child

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        if children is None: return
        for child in children:
            self.add_child(child)

    def remove_child(self, child):
        self.children.remove(child)

    def remove_children(self, children):
        if children is None: return
        for child in children:
            self.remove_child(child)

    def clear_children(self):
        self.children = set()

    def iterate(self):
        for item in self.children:
            yield item
            for i in item.iterate():
                yield i

class GraphItem:
    def __init__(self):
        self.next = None
        self.prev = None
        self.parent = None
        self.children = []
        self.dependers = set()
        self.dependencies = set()

    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next
        self.next.prev = self

    def get_parent(self):
        return self.parent

    def _set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        for child in self.children:
            yield child

    def add_child(self, child):
        self.children.append(child)
        child._set_parent(self)

    def add_children(self, children):
        if children is None: return
        for child in children:
            self.add_child(child)

    def remove_child(self, child):
        self.children.remove(child)
        child._set_parent(None)

    def remove_children(self, children):
        if children is None: return
        for child in children:
            self.remove_child(child)

    def clear_children(self):
        self.remove_children(self.get_children())

    def get_dependers(self):
        return sorted(self.dependers)

    def add_depender(self, depender):
        self.dependers.add(depender)

    def add_dependers(self, dependers):
        if dependers is None: return
        for depender in dependers:
            self.add_depender(depender)

    def remove_depender(self, depender):
        self.dependers.remove(depender)

    def remove_dependers(self, dependers):
        if dependers is None: return
        for depender in dependers:
            self.remove_depender(depender)

    def clear_dependencies(self):
        self.dependencies = set()

    def get_dependencies(self):
        return sorted(self.dependencies)

    def add_dependency(self, dependency):
        self.dependencies.add(dependency)

    def add_dependencies(self, dependencies):
        if dependencies is None: return
        for dependency in dependencies:
            self.add_dependency(dependency)

    def remove_dependency(self, dependency):
        self.dependencies.remove(dependency)

    def remove_dependencies(self, dependencies):
        if dependencies is None: return
        for dependency in dependencies:
            self.remove_dependency(dependency)

    def clear_dependencies(self):
        self.dependencies = set()

    def iterate(self):
        for item in self.children:
            yield item
            for i in item.iterate():
                yield i

    def depth(self):
        d = 0
        i = self
        while i.parent:
            i = i.parent
            d += 1
        return d
