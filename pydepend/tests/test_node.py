import unittest
import ast

from ..node import Node


class TestNode(unittest.TestCase):
    def test_basic_properties(self):
        node = Node('name', ast.parse('ast'), 'file.txt')

        self.assertEqual('name', node.name)
        self.assertEqual('ast', node.ast.body[0].value.id)
        self.assertEqual('file.txt', node.filename)
