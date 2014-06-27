import unittest

from ..table import Row, Table


class TestRow(unittest.TestCase):
    def setUp(self):
        self.columns = ['id', 'name']
        self.values = {'id': 1, 'name': 'hello world'}
        self.row = Row(self.columns, self.values)

    def test_dictlike(self):
        self.assertEqual(2, len(self.row))
        self.assertListEqual(self.columns, list(self.row.keys()))
        self.assertDictEqual(self.values, dict(self.row))

    def test_access_by_index(self):
        self.assertEqual(1, self.row[0])
        self.assertEqual('hello world', self.row[1])


class TestTable(unittest.TestCase):
    def setUp(self):
        self.columns = ['id', 'name']
        self.table = Table(self.columns)

        self.table.add_row(1, 'hello1')
        self.table.add_row(id=2, name='hello2')
        self.table.add_row(3, name='hello3')

    def test_sequence_like(self):
        self.assertEqual(3, len(self.table))
        self.assertListEqual([Row(self.columns, {'id': 1, 'name': 'hello1'}),
                              Row(self.columns, {'id': 2, 'name': 'hello2'}),
                              Row(self.columns, {'id': 3, 'name': 'hello3'})], list(self.table))
