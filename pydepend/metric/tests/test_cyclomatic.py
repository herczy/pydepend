import unittest
import ast

from ..cyclomatic import cyclomatic_complexity


class TestCyclomatic(unittest.TestCase):
    def test_simple_statement(self):
        self.assertEqual(0, cyclomatic_complexity('print("hello")'))

    def test_simple_if(self):
        self.assertEqual(1, cyclomatic_complexity('if a:\n\treturn 1'))

    def test_if_with_else(self):
        self.assertEqual(1, cyclomatic_complexity('if a:\n\treturn 1\nelse:\n\treturn 0'))

    def test_if_with_elif(self):
        self.assertEqual(2, cyclomatic_complexity('if a:\n\treturn 1\nelif b:\n\treturn 0'))

    def test_for(self):
        self.assertEqual(1, cyclomatic_complexity('for a in range(1):\n\treturn 1'))

    def test_while(self):
        self.assertEqual(1, cyclomatic_complexity('while True:\n\treturn 1'))

    def test_try_with_except(self):
        self.assertEqual(1, cyclomatic_complexity('try:\n\t1\nexcept:\n\t2'))

    def test_try_with_finally(self):
        self.assertEqual(1, cyclomatic_complexity('try:\n\t1\nfinally:\n\t2'))

    def test_last_return_statement(self):
        self.assertEqual(0, cyclomatic_complexity('def func():\n\treturn'))

    def test_non_last_return_statement(self):
        self.assertEqual(1, cyclomatic_complexity('def func():\n\treturn\n\t1'))

    def test_nested_non_last_return_statement(self):
        self.assertEqual(2, cyclomatic_complexity('def func():\n\tif a:\n\t\treturn 1'))
        self.assertEqual(2, cyclomatic_complexity('def func():\n\tif a:\n\t\treturn 1\n\treturn 0'))

    def test_func_with_no_return(self):
        self.assertEqual(0, cyclomatic_complexity('def func():\n\tpass'))

    def test_break_in_loop(self):
        self.assertEqual(2, cyclomatic_complexity('while True:\n\tbreak'))

    def test_continue_in_loop(self):
        self.assertEqual(2, cyclomatic_complexity('while True:\n\tcontinue'))

    def test_ternary_operator(self):
        self.assertEqual(1, cyclomatic_complexity('a if b else c'))

    def test_binary_and(self):
        self.assertEqual(1, cyclomatic_complexity('a and b'))

    def test_binary_or(self):
        self.assertEqual(1, cyclomatic_complexity('a or b'))

    def test_visit_preparsed(self):
        self.assertEqual(1, cyclomatic_complexity(ast.parse('if a:\n\t1')))
