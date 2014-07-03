import ast


class Node(object):
    def __init__(self, ast, parent=None):
        self.__ast = ast
        self.__parent = parent

    @property
    def ast(self):
        return self.__ast

    @property
    def parent(self):
        return self.__parent

    @property
    def root(self):
        if self.__parent is not None:
            return self.__parent.root

        return self


class TerminalNode(Node):
    def __init__(self, name, ast, filename, parent=None):
        super(TerminalNode, self).__init__(ast, parent=parent)

        self.__name = name
        self.__filename = filename

    @property
    def name(self):
        return self.__name

    @property
    def filename(self):
        return self.__filename
