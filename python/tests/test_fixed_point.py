import unittest

from src.quantize import quantize, scale, Rounding


class TestFixedPoint(unittest.TestCase):

    def test_fixed(self):
        with self.assertRaises(ValueError) as context:
            quantize(1.0, 0)
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)
        with self.assertRaises(ValueError) as context:
            quantize(1.0, -0.1)
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)

        self.assertEqual(quantize(0.1, 1.0), 0)
        self.assertEqual(quantize(1.0, 1.0), 1)
        self.assertEqual(quantize(10.0, 1.0), 10)

        self.assertEqual(quantize(0.26, 0.5), 1)
        self.assertEqual(quantize(0.25, 0.5), 0)  # rounds down
        self.assertEqual(quantize(0.24, 0.5), 0)

        self.assertEqual(quantize(1.26, 0.5, Rounding.DOWN), 2)
        self.assertEqual(quantize(1.25, 0.5, Rounding.DOWN), 2)
        self.assertEqual(quantize(1.24, 0.5, Rounding.DOWN), 2)

        self.assertEqual(quantize(1.26, 0.5, Rounding.UP), 3)
        self.assertEqual(quantize(1.25, 0.5, Rounding.UP), 3)
        self.assertEqual(quantize(1.24, 0.5, Rounding.UP), 3)

        self.assertEqual(quantize(1.26e-9, 0.5e-9), 3)
        self.assertEqual(quantize(1.25e-9, 0.5e-9), 2)
        self.assertEqual(quantize(1.24e-9, 0.5e-9), 2)

    def test_floating(self):
        with self.assertRaises(ValueError) as context:
            scale(1, 0)
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)
        with self.assertRaises(ValueError) as context:
            scale(1, -0.1)
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)

        self.assertEqual(scale(0, 1.0), 0)
        self.assertEqual(scale(1, 1.0), 1.0)
        self.assertEqual(scale(10, 1.0), 10.0)

        self.assertEqual(scale(1, 0.5), 0.5)
        self.assertEqual(scale(0, 0.5), 0)

        # need almost equals since value cannot be represented as binary fractions
        # https://docs.python.org/3/tutorial/floatingpoint.html
        self.assertAlmostEqual(scale(3, 0.5e-9), 1.5e-9, places=9)
        self.assertAlmostEqual(scale(2, 0.5e-9), 1.0e-9, places=9)
