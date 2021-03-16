import unittest

from src.circuit_search_common import Range, Param


class TestCircuitSearchCommon(unittest.TestCase):

    def test_range(self):
        with self.assertRaises(ValueError) as context:
            Range(Param.WIDTH, 2.0, 1.0, 1.0)
            self.assertIn("Range low must be less than or equal to high", context.exception.args)

        with self.assertRaises(ValueError) as context:
            Range(Param.WIDTH, 1, 2.0, 1.0)
            self.assertIn("Range low and high must be the same type", context.exception.args)

        self.assertEqual(list(Range(Param.FINGERS, 1, 6, 1)), [1, 2, 3, 4, 5, 6])
        self.assertEqual(list(Range(Param.FINGERS, 1, 6, 2)), [1, 3, 5])

        self.assertEqual(list(Range(Param.WIDTH, 1.0, 6.0, 1.0)), [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        self.assertEqual(list(Range(Param.FINGERS, 1, 6, 2)), [1, 3, 5])
