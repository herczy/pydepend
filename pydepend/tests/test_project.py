import io
import sys
import unittest

from ..ext.cyclomatic import CyclomaticComplexity
from ..node import ModuleNode
from ..project import Project
from ..report import Report
from . import get_asset_path


class FakeReport(Report):
    results = None

    def report(self, results):
        self.results = results
        return 'report'


if sys.version_info.major >= 3:
    StringIO = io.StringIO

else:
    StringIO = io.BytesIO


class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project(path=(get_asset_path('.'),))
        self.project.add_package('testfile')
        self.project.add_package('testpackage')

        self.metric = CyclomaticComplexity()
        self.project.add_metric(self.metric)

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

    def test_metrics(self):
        self.assertTupleEqual((self.metric,), self.project.metrics)

    def test_make_report(self):
        report = FakeReport()
        stdout = StringIO()
        self.project.set_report(report)
        self.project.report(stream=stdout)

        self.assertEqual('report', stdout.getvalue())
        self.assertSetEqual(
            {'testfile', 'testpackage', 'testpackage.testmod'},
            set(report.results.keys())
        )

    def test_init_with_default_values(self):
        self.assertTupleEqual(tuple(sys.path), Project().path)
