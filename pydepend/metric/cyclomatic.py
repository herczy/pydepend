import ast
import collections

from ..visitor import ClassVisitor, handle
from ..node import Node

from . import Metric


class _TypeCountVisitor(ClassVisitor):
    @handle(ast.AST)
    def __visit_ast(self, node):
        return (node.__class__,) + tuple(cls for name in node._fields for cls in self.visit(getattr(node, name)))

    @handle(collections.Sequence)
    def __visit_sequence(self, node):
        return tuple(cls for entry in node for cls in self.visit(entry))

    @handle(str)
    def __visit_str(self, node):
        return ()

    def default(self, node):
        return ()

    @classmethod
    def count(cls, node):
        res = {}

        for entry in cls().visit(node):
            res.setdefault(entry, 0)
            res[entry] += 1

        return res


class _CyclomaticVisitor(ClassVisitor):
    @handle(
        ast.If,
        ast.IfExp,
        ast.For,
        ast.While,
        ast.TryExcept,
        ast.TryFinally,
        ast.Break,
        ast.Continue,
        ast.And,
        ast.Or
    )
    def __visit_selected(self, node):
        return 1 + self.__visit_ast(node)

    @handle(ast.FunctionDef)
    def __visit_function(self, node):
        count = _TypeCountVisitor.count(node).get(ast.Return, 0)
        if isinstance(node.body[-1], ast.Return):
            count -= 1

        return count + self.__visit_ast(node)

    @handle(ast.AST)
    def __visit_ast(self, node):
        return sum(self.visit(getattr(node, name)) for name in node._fields)

    @handle(collections.Sequence)
    def __visit_sequence(self, node):
        return sum(self.visit(entry) for entry in node)

    @handle(str)
    def __visit_str(self, node):
        return 0

    def default(self, node):
        return 0


class CyclomaticComplexity(Metric):
    def calculate(self, node):
        return _CyclomaticVisitor().visit(node.ast)
