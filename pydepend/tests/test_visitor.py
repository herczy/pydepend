import unittest
import collections

from ..visitor import ClassVisitor, handle


class TestClassVisitor(unittest.TestCase):
    def assert_visitation(self, expected_key, value):
        visited_type, visited_value, args, kwargs = ExampleClassVisitor().visit(value, 2, a=3)

        self.assertEqual(expected_key, visited_type)
        self.assertEqual(value, visited_value)
        self.assertEqual((2,), args)
        self.assertEqual({'a': 3}, kwargs)

    def test_visit_int(self):
        self.assert_visitation(int, 1)

    def test_visit_bool(self):
        self.assert_visitation(bool, True)

    def test_visit_subtype(self):
        self.assert_visitation(collections.Sequence, ())

    def test_visit_special_subtype(self):
        self.assert_visitation(str, 'hello')

    def test_visit_default(self):
        self.assert_visitation('default', object())

    def test_visit_default_standard_operation(self):
        self.assertRaises(TypeError, ClassVisitor().visit, 1)


class ExampleClassVisitor(ClassVisitor):
    @handle(int)
    def visit_int(self, value, *args, **kwargs):
        return (int, value, args, kwargs)

    @handle(bool)
    def visit_bool(self, value, *args, **kwargs):
        return (bool, value, args, kwargs)

    @handle(collections.Sequence)
    def visit_seq(self, value, *args, **kwargs):
        return (collections.Sequence, value, args, kwargs)

    @handle(str)
    def visit_str(self, value, *args, **kwargs):
        return (str, value, args, kwargs)

    def default(self, value, *args, **kwargs):
        return ('default', value, args, kwargs)
