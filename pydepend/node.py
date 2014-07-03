import ast


class Node(object):
    def __init__(self, ast):
        self.__ast = ast

    @property
    def ast(self):
        return self.__ast


class TerminalNode(Node):
    def __init__(self, name, ast, filename):
        super(TerminalNode, self).__init__(ast)

        self.__name = name
        self.__filename = filename

    @property
    def name(self):
        return self.__name

    @property
    def filename(self):
        return self.__filename
