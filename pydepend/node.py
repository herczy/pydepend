import ast


class Node(object):
    def __init__(self, name, ast, parent=None):
        self.__name = name
        self.__ast = ast
        self.__parent = parent

    @property
    def name(self):
        return self.__name

    @property
    def ast(self):
        return self.__ast

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
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


class ModuleNode(ContainerNode):
    def __init__(self, name, ast, filename, children, parent=None):
        super(ModuleNode, self).__init__(name, ast, children, parent=parent)

        self.__filename = filename

    @property
    def filename(self):
        return self.__filename


class TerminalNode(Node):
    def __init__(self, name, ast, filename, parent=None):
        super(TerminalNode, self).__init__(name, ast, parent=parent)

        self.__filename = filename

    @property
    def filename(self):
        return self.__filename
