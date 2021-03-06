import unittest
import ast

from ..node import Node, ContainerNode, ModuleNode


class TestNode(unittest.TestCase):
    def setUp(self):
        self.ast = ast.parse('ast').body[0]
        self.parent = Node('root', None)
        self.node = Node('name', self.ast, parent=self.parent)

    def test_name(self):
        self.assertEqual('name', self.node.name)

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

    def test_set_invalid_parent_in_constructor(self):
        self.assertRaises(TypeError, Node, 'name', self.ast, parent=1)

    def test_set_invalid_parent_with_setter(self):
        with self.assertRaises(TypeError):
            self.node.parent = 1

    def test_full_name(self):
        self.assertEqual('root.name', self.node.fullname)


class TestContainerNode(unittest.TestCase):
    def setUp(self):
        self.children = [Node('child', None)]
        self.node = ContainerNode('container', ast.parse('ast'), self.children)

    def test_children(self):
        self.assertTupleEqual(tuple(self.children), self.node.children)

    def test_parents_of_children_are_updated(self):
        self.assertEqual(self.node, self.children[0].parent)

    def test_resolve_child_by_name(self):
        root_node = ContainerNode('root', None, [self.node])

        self.assertEqual(self.children[0], root_node.resolve('container.child'))

    def test_resolve_unknown(self):
        self.assertRaises(KeyError, self.node.resolve, 'unknown')

    def test_walk(self):
        node0 = Node('node0', None)
        node1 = Node('node1', None)
        node2 = ContainerNode('node2', None, [node0, node1])
        node3 = Node('node3', None)
        node4 = ContainerNode('node4', None, [node2, node3])

        self.assertListEqual([node4, node2, node0, node1, node3],
                             list(node4.walk()))


class TestModuleNode(unittest.TestCase):
    def setUp(self):
        self.children = [Node('child', None)]
        self.node = ModuleNode('name', None, 'file.txt', self.children)

    def test_filename(self):
        self.assertEqual('file.txt', self.node.filename)

    def test_children(self):
        self.assertTupleEqual(tuple(self.children), self.node.children)
