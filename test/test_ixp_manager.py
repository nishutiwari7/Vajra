import unittest
from ixp_manager import IXPManager

class TestIXPManager(unittest.TestCase):
    def setUp(self):
        self.ixp_manager = IXPManager()

    def test_access_ixp(self):
        result = self.ixp_manager.access_ixp("network1")
        self.assertTrue(result, "IXP access should succeed")

    def test_prevent_duplicate_access(self):
        self.ixp_manager.access_ixp("network1")
        with self.assertRaises(Exception, msg="Duplicate access should raise an exception"):
            self.ixp_manager.access_ixp("network1")
