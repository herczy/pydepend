import ast
import unittest

from ..tests import get_asset_path
from ..collector import Collector, Node


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

        self.collector = Collector(self.example)

    def test_empty(self):
        self.assertEqual({}, dict(Collector()))

    def __assert_node(self, key, ast_type, filename=None):
        if filename is not None:
            filename = get_asset_path(filename)

        node = self.collector[key]
        self.assertIsInstance(node, Node)
        self.assertIsInstance(node.ast, ast_type)
        self.assertEqual(key, node.name)
        self.assertEqual(filename, node.filename)

    def test_simple_function(self):
        self.__assert_node('outer', ast.FunctionDef)

    def test_class_method(self):
        self.__assert_node('OuterClass.method0', ast.FunctionDef)

    def test_class(self):
        self.__assert_node('OuterClass', ast.ClassDef)

    def test_keys_sorted_by_lineno(self):
        self.assertListEqual(['OuterClass', 'OuterClass.method0', 'OuterClass.method1', 'outer'],
                             list(self.collector.keys()))

    def test_collect_file(self):
        self.collector = Collector.load_from_path(get_asset_path('testfile.py'))

        self.__assert_node('testfile.outerfunc', ast.FunctionDef, filename='testfile.py')

    def test_collect_file_in_module(self):
        self.collector = Collector.load_from_path(get_asset_path('testpackage/testmod.py'))

        self.__assert_node('testpackage.testmod.func', ast.FunctionDef, filename='testpackage/testmod.py')

    def test_collect_module_func(self):
        self.collector = Collector.load_from_path(get_asset_path('testpackage/__init__.py'))

        self.__assert_node('testpackage.initfunc', ast.FunctionDef, filename='testpackage/__init__.py')

    def test_collect_package(self):
        self.collector = Collector.load_from_path(get_asset_path('testpackage'))

        self.__assert_node('testpackage.testmod.func', ast.FunctionDef, filename='testpackage/testmod.py')
        self.__assert_node('testpackage.initfunc', ast.FunctionDef, filename='testpackage/__init__.py')
