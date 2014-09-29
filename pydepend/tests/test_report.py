import unittest

from ..report import Result, ResultCollection


class TestResult(unittest.TestCase):
    def setUp(self):
        self.name = 'fully.qualified.object.name'
        self.metrics = {'Some metric': 123, 'Some other metric': 321}
        self.result = Result(self.name, self.metrics)

    def test_name(self):
        self.assertEqual(self.name, self.result.name)

    def test_complexity(self):
        self.assertDictEqual(self.metrics, self.result.metrics)

    def test_complexity_is_immutable(self):
        self.result.metrics['a'] = 2
        expected = dict(self.metrics)
        self.metrics['x'] = 2

        self.assertDictEqual(expected, self.result.metrics)

    def test_equality(self):
        self.assertEqual(Result(self.name, self.metrics), self.result)
        self.assertNotEqual(Result('x', self.metrics), self.result)
        self.assertNotEqual(Result(self.name, {}), self.result)
        self.assertNotEqual(object(), self.result)

    def test_stringify(self):
        self.assertEqual(
            "fully.qualified.object.name('Some metric' => 123, 'Some other metric' => 321)",
            str(self.result)
        )
        self.assertEqual(
            "Result(fully.qualified.object.name: 'Some metric' => 123, 'Some other metric' => 321)",
            repr(self.result)
        )


class TestResultCollection(unittest.TestCase):
    def setUp(self):
        self.metrics = {'x': 1, 'y': 2}
        self.results = ResultCollection()
        self.results.add(Result('a', self.metrics))
        self.results.add(Result('b', self.metrics))

    def test_dictlike(self):
        expected = {
            'a': Result('a', self.metrics),
            'b': Result('b', self.metrics),
        }

        self.assertDictEqual(expected, dict(self.results))

    def test_keep_result_order(self):
        self.results.add(Result(0, self.metrics))

        self.assertListEqual(['a', 'b', 0], list(self.results))
