import unittest

from ..resolver import DependencyTable, CircularDependencyError, UnknownDependencyError


class TestDependencyTable(unittest.TestCase):
    def test_resolve_in_empty_table(self):
        self.assertRaises(UnknownDependencyError, DependencyTable().resolve, ['anyname'])

    def test_resolve_independent_modules(self):
        self.assertEqual(
            [{'name0', 'name1'}],
            DependencyTable(
                {
                    'name0': (),
                    'name1': (),
                }
            ).resolve(['name0', 'name1'])
        )

    def test_resolve_interdependent_modules(self):
        self.assertEqual(
            [{'name0'}, {'name1'}],
            DependencyTable(
                {
                    'name1': ('name0',),
                    'name0': (),
                }
            ).resolve(['name1'])
        )

    def test_resolve_circular_dependency(self):
        self.assertRaises(
            CircularDependencyError,
            DependencyTable,
            {
                'name0': ('name1',),
                'name1': ('name0',),
            }
        )

    def test_create_with_unknown_dependencies(self):
        self.assertRaises(
            UnknownDependencyError,
            DependencyTable,
            {
                'name0': ('name1',),
            }
        )

    DIAMOND_DEPENDENCY = {
        'target': ('intermed0', 'intermed1', 'lowlevel'),
        'intermed0': ('lowlevel',),
        'intermed1': ('lowlevel',),
        'lowlevel': (),
    }

    DIAMOND_ORDER = [{'lowlevel'}, {'intermed0', 'intermed1'}, {'target'}]

    def test_resolve_diamond_dependencies(self):
        self.assertEqual(
            self.DIAMOND_ORDER, 
            DependencyTable(self.DIAMOND_DEPENDENCY).resolve(['target'])
        )

    def assert_after(self, where, first, last):
        self.assertTrue(
            where.index(first) < where.index(last),
            msg='Expected {!r} to come before {!r}'.format(first, last)
        )

    def test_resolve_flat(self):
        resolved = DependencyTable(self.DIAMOND_DEPENDENCY).resolve(['target'], flat=True)

        self.assert_after(resolved, 'lowlevel', 'intermed0')
        self.assert_after(resolved, 'lowlevel', 'intermed1')
        self.assert_after(resolved, 'intermed0', 'target')
        self.assert_after(resolved, 'intermed1', 'target')

    def test_resolve_all(self):
        self.assertEqual(
            self.DIAMOND_ORDER, 
            DependencyTable(self.DIAMOND_DEPENDENCY).resolve_all()
        )

    def test_resolve_all_flat(self):
        resolved = DependencyTable(self.DIAMOND_DEPENDENCY).resolve_all(flat=True)

        self.assert_after(resolved, 'lowlevel', 'intermed0')
        self.assert_after(resolved, 'lowlevel', 'intermed1')
        self.assert_after(resolved, 'intermed0', 'target')
        self.assert_after(resolved, 'intermed1', 'target')
