import unittest

from ..node import ModuleNode
from ..project import Project
from . import get_asset_path


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project(path=(get_asset_path('.'),))
        self.project.add_package('testfile')
        self.project.add_package('testpackage')

    def __assert_modules(self, expected, packages, path=None):
        path = path or [get_asset_path('.')]

        project = Project(path=path)
        for package in packages:
            project.add_package(package)

        self.assertSetEqual(set(expected), set(project.modules))

    def test_load_module(self):
        self.__assert_modules(['testfile'], ['testfile'])

    def test_load_package(self):
        self.__assert_modules(['testpackage', 'testpackage.testmod'], ['testpackage'])

    def test_load_submodule(self):
        self.__assert_modules(['testpackage.testmod'], ['testpackage.testmod'])

    def test_load_submodule_with_different_import_path(self):
        self.__assert_modules(['testpackage.testmod'], ['testmod'], path=[get_asset_path('testpackage')])

    def test_get_module_node(self):
        node = self.project.get_module_node('testfile')

        self.assertIsInstance(node, ModuleNode)
        self.assertEqual('testfile', node.name)
        self.assertEqual(get_asset_path('testfile.py'), node.filename)
