import unittest
from monitor import getListOfProcessSortedByMemory


class TestMemoryUsage(unittest.TestCase):
    def test_getListOfProcessSortedByMemory(self):
        self.assertEqual(list, type(getListOfProcessSortedByMemory()))
        self.assertEqual(dict, type(getListOfProcessSortedByMemory()[0]))
        self.assertLessEqual(1, len(getListOfProcessSortedByMemory()))
