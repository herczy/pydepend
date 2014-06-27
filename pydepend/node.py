import ast


class Node(object):
    def __init__(self, name, ast, filename):
        self.__name = name
        self.__ast = ast
        self.__filename = filename

    @property
    def name(self):
        return self.__name

    @property
    def ast(self):
        return self.__ast

    @property
    def filename(self):
        return self.__filename
