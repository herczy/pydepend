import os.path
import ast

from . import node
from .visitor import ClassVisitor, handle


class Collector(ClassVisitor):
    @classmethod
    def collect_from_file(cls, filename):
        if os.path.isdir(filename):
            filename = os.path.join(filename, '__init__.py')

        with open(filename) as f:
            return cls.collect_from_ast(ast.parse(f.read()), filename=filename)

    @classmethod
    def collect_from_ast(cls, obj, filename=None):
        return cls(filename).visit(obj)

    def __init__(self, filename):
        super(Collector, self).__init__()

        self.__filename = filename

        dirname, filename = os.path.split(filename)
        name = os.path.splitext(filename)[0]
        if name == '__init__':
            name = os.path.basename(dirname)

        self.__name = name

    @handle(ast.Module)
    def visit_module(self, obj):
        children = self.__visit_and_filter_nones(obj.body)
        return node.ModuleNode(self.__name, obj, self.__filename, children)

    @handle(ast.FunctionDef)
    def visit_function_definition(self, obj):
        return node.Node(obj.name, obj)

    @handle(ast.ClassDef)
    def visit_class_definition(self, obj):
        return node.ContainerNode(obj.name, obj, children=self.__visit_and_filter_nones(obj.body))

    def default(self, node):
        pass

    def __visit_and_filter_nones(self, seq):
        for entry in seq:
            res = self.visit(entry)
            if res is not None:
                yield res
