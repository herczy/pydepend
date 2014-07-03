import unittest
import ast

from ..node import Node, TerminalNode


class TestNode(unittest.TestCase):
    def setUp(self):
        self.ast = ast.parse('ast').body[0]
        self.parent = Node(None)
        self.node = Node(self.ast, parent=self.parent)

    def test_ast(self):
        self.assertEqual(self.ast, self.node.ast)

    def test_parent(self):
        self.assertEqual(self.parent, self.node.parent)

    def test_root(self):
        self.assertEqual(self.parent, self.node.root)

    def test_root_of_root(self):
        self.assertEqual(self.parent, self.parent.root)


class TestTerminalNode(unittest.TestCase):
    def setUp(self):
        self.ast = ast.parse('ast').body[0]
        self.node = TerminalNode('name', self.ast, 'file.txt')

    def test_name(self):
        self.assertEqual('name', self.node.name)

    def test_filename(self):
        self.assertEqual('file.txt', self.node.filename)
