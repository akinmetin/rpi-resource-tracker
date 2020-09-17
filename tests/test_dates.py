import unittest
from monitor import getDate, getDateTime


class TestDates(unittest.TestCase):
    def test_getDate(self):
        self.assertEqual(str, type(getDate()))

    def test_getDateTime(self):
        self.assertEqual(str, type(getDateTime()))
