import os.path
import unittest
import pydepend

from . import get_asset_path
from .. import util


PYDEPEND_BASE_PATH = os.path.dirname(pydepend.__file__)


class TestUtil(unittest.TestCase):
    def test_scan(self):
        basepath = get_asset_path('testpackage/nonpackagedir')
        paths = set(util.scan(basepath))

        self.assertIn(os.path.join(basepath, 'somefile.py'), paths)

    def test_scan_multilevel(self):
        basepath = get_asset_path('testpackage')
        paths = set(util.scan(basepath))

        self.assertIn(os.path.join(basepath, 'nonpackagedir/somefile.py'), paths)
        self.assertIn(os.path.join(basepath, 'nonpackagedir'), paths)
        self.assertIn(os.path.join(basepath, 'nonpythonfile.txt'), paths)

    def test_redule_top_level_package(self):
        self.assertEqual(
            (os.path.dirname(PYDEPEND_BASE_PATH), 'pydepend'),
            util.reduce_package_name(PYDEPEND_BASE_PATH)
        )

    def test_reduce_complex_name(self):
        self.assertEqual(
            (os.path.dirname(PYDEPEND_BASE_PATH), 'pydepend.tests.test_util'),
            util.reduce_package_name(__file__)
        )

    def test_reduce_non_python_name(self):
        self.assertRaises(
            util.NotAPythonModuleError,
            util.reduce_package_name,
            get_asset_path('testpackage/nonpythonfile.txt')
        )
        self.assertRaises(
            util.NotAPythonModuleError,
            util.reduce_package_name,
            get_asset_path('testpackage/nonpackagedir')
        )
