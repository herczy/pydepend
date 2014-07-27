import ast


class Node(object):
    __parent = None

    def __init__(self, name, ast, parent=None):
        self.__name = name
        self.__ast = ast

        self.parent = parent

    @property
    def name(self):
        return self.__name

    @property
    def fullname(self):
        if self.__parent is None:
            return self.__name

        return self.__parent.name + '.' + self.__name

    @property
    def ast(self):
        return self.__ast

    @property
    def parent(self):
        return self.__parent

    def __validate_parent_value(self, value):
        if value is not None and not isinstance(value, Node):
            raise TypeError('Expected node type or None, instead of {}'.format(type(value).__name__))

    @parent.setter
    def parent(self, value):
        self.__validate_parent_value(value)
        self.__parent = value

    @parent.deleter
    def parent(self):
        self.__parent = None

    @property
    def root(self):
        if self.__parent is not None:
            return self.__parent.root

        return self


class ContainerNode(Node):
    def __init__(self, name, ast, children, parent=None):
        super(ContainerNode, self).__init__(name, ast, parent=parent)

        self.__children = tuple(children)
        for child in self.__children:
            child.parent = self

    @property
    def children(self):
        return self.__children

    def __get_child_by_name(self, name):
        for child in self.children:
            if child.name == name:
                return child

        raise KeyError(name)

    def resolve(self, fq_name):
        res = self
        for comp in fq_name.split('.'):
            res = res.__get_child_by_name(comp)

        return res

    def walk(self):
        yield self

        for child in self.__children:
            if isinstance(child, ContainerNode):
                for res in child.walk():
                    yield res

            else:
                yield child


class ModuleNode(ContainerNode):
    def __init__(self, name, ast, filename, children, parent=None):
        super(ModuleNode, self).__init__(name, ast, children, parent=parent)

        self.__filename = filename

    @property
    def filename(self):
        return self.__filename
