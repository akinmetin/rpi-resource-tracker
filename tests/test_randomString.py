import unittest
from monitor import get_random_alphanumeric_string


class TestRandomString(unittest.TestCase):
    def test_random_string(self):
        self.assertEqual(str, type(get_random_alphanumeric_string()))
