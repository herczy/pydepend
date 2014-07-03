import unittest
import ast

from ...node import Node

from ..cyclomatic import CyclomaticComplexity


class TestCyclomatic(unittest.TestCase):
    def setUp(self):
        self.metric = CyclomaticComplexity()

    def assert_complexity(self, complexity, code):
        node = Node('__global__', ast.parse(code))
        self.assertEqual(complexity, self.metric.calculate(node))

    def test_simple_statement(self):
        self.assert_complexity(0, 'print("hello")')

    def test_simple_if(self):
        self.assert_complexity(1, 'if a:\n\treturn 1')

    def test_if_with_else(self):
        self.assert_complexity(1, 'if a:\n\treturn 1\nelse:\n\treturn 0')

    def test_if_with_elif(self):
        self.assert_complexity(2, 'if a:\n\treturn 1\nelif b:\n\treturn 0')

    def test_for(self):
        self.assert_complexity(1, 'for a in range(1):\n\treturn 1')

    def test_while(self):
        self.assert_complexity(1, 'while True:\n\treturn 1')

    def test_try_with_except(self):
        self.assert_complexity(1, 'try:\n\t1\nexcept:\n\t2')

    def test_try_with_finally(self):
        self.assert_complexity(1, 'try:\n\t1\nfinally:\n\t2')

    def test_last_return_statement(self):
        self.assert_complexity(0, 'def func():\n\treturn')

    def test_non_last_return_statement(self):
        self.assert_complexity(1, 'def func():\n\treturn\n\t1')

    def test_nested_non_last_return_statement(self):
        self.assert_complexity(2, 'def func():\n\tif a:\n\t\treturn 1')
        self.assert_complexity(2, 'def func():\n\tif a:\n\t\treturn 1\n\treturn 0')

    def test_func_with_no_return(self):
        self.assert_complexity(0, 'def func():\n\tpass')

    def test_break_in_loop(self):
        self.assert_complexity(2, 'while True:\n\tbreak')

    def test_continue_in_loop(self):
        self.assert_complexity(2, 'while True:\n\tcontinue')

    def test_ternary_operator(self):
        self.assert_complexity(1, 'a if b else c')

    def test_binary_and(self):
        self.assert_complexity(1, 'a and b')

    def test_binary_or(self):
        self.assert_complexity(1, 'a or b')
