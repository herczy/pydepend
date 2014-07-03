import unittest
import ast

from ..node import Node, TerminalNode


class TestNode(unittest.TestCase):
    def setUp(self):
        self.ast = ast.parse('ast').body[0]
        self.node = Node(self.ast)

    def test_ast(self):
        self.assertEqual(self.ast, self.node.ast)


class TestTerminalNode(unittest.TestCase):
    def setUp(self):
        self.ast = ast.parse('ast').body[0]
        self.node = TerminalNode('name', self.ast, 'file.txt')

    def test_name(self):
        self.assertEqual('name', self.node.name)

    def test_filename(self):
        self.assertEqual('file.txt', self.node.filename)
