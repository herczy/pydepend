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

    def test_change_parent(self):
        self.node.parent = None

        self.assertEqual(None, self.node.parent)

    def test_delete_parent(self):
        del self.node.parent

        self.assertEqual(None, self.node.parent)

class TestTerminalNode(unittest.TestCase):
    def setUp(self):
        self.node = TerminalNode('name', None, 'file.txt')

    def test_name(self):
        self.assertEqual('name', self.node.name)

    def test_filename(self):
        self.assertEqual('file.txt', self.node.filename)