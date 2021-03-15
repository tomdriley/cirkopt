import unittest

from src.brute_force_search import Range, Param


class TestBruteForceSearch(unittest.TestCase):

    def test_range(self):
        with self.assertRaises(ValueError) as context:
            Range(Param.WIDTH, 2.0, 1.0, 1.0)
            self.assertIn("Range low must be less than or equal to high", context.exception.args)

        with self.assertRaises(ValueError) as context:
            Range(Param.WIDTH, 1, 2.0, 1.0)
            self.assertIn("Range low and high must be the same type", context.exception.args)

        self.assertEqual(list(Range(Param.WIDTH, 1, 6, 1)), [1, 2, 3, 4, 5, 6])
        self.assertEqual(list(Range(Param.WIDTH, 1, 6, 2)), [1, 3, 5])

        self.assertEqual(list(Range(Param.WIDTH, 1.0, 6.0, 1.0)), [1, 2, 3, 4, 5, 6])
        self.assertEqual(list(Range(Param.WIDTH, 1, 6, 2)), [1, 3, 5])
