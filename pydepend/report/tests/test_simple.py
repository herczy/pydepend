import unittest

from .. import Result, ResultCollection
from ..simple import SimpleReport


class TestSimpleReport(unittest.TestCase):
    def test_create(self):
        pass

    def setUp(self):
        self.results = ResultCollection()
        self.results.add(Result('a', {'x': 1, 'y': 2}))
        self.results.add(Result('b', {'x': 3, 'y': 4}))
        self.report = SimpleReport()

    def test_report(self):
        expected = '''\
a: x = 1, y = 2
b: x = 3, y = 4
'''

        self.assertEqual(expected, self.report.report(self.results))
