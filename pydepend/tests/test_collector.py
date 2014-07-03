import ast
import unittest

from ..tests import get_asset_path
from ..collector import Collector
from .. import node


class TestCollector(unittest.TestCase):
    def setUp(self):
        self.example = '''
class OuterClass(object):
    def method0(self):
        return 0
        
    def method1(self):
        if a:
            return 1
            
        return 2

def outer():
    if a:
        return 1

    else:
        return 2

    return 0'''

        self.node = Collector.collect_from_ast(ast.parse(self.example), filename='package/base/module.py')

    def __assert_node(self, node, name, ast_type, node_type=node.Node):
        self.assertIsInstance(node, node_type)
        self.assertEqual(name, node.name)
        self.assertIsInstance(node.ast, ast_type)

    def test_global_node(self):
        self.__assert_node(self.node, 'module', ast.Module, node.ModuleNode)
        self.assertEqual('package/base/module.py', self.node.filename)

    def test_outer_function(self):
        self.__assert_node(self.node.resolve('outer'), 'outer', ast.FunctionDef)

    def test_outer_class(self):
        self.__assert_node(self.node.resolve('OuterClass'), 'OuterClass', ast.ClassDef, node_type=node.ContainerNode)

    def test_method(self):
        self.__assert_node(self.node.resolve('OuterClass.method1'), 'method1', ast.FunctionDef)

    def test_init_file(self):
        pkg = Collector.collect_from_ast(ast.parse(self.example), filename='package/__init__.py')

        self.__assert_node(pkg, 'package', ast.Module, node_type=node.ModuleNode)
