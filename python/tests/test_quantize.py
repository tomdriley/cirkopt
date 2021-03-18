import unittest
from decimal import Decimal as d

from src.quantize import quantize, scale, Rounding


class TestQuantize(unittest.TestCase):

    def test_quantize(self):
        with self.assertRaises(ValueError) as context:
            quantize(d(1.0), d('0'))
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)
        with self.assertRaises(ValueError) as context:
            quantize(d(1.0), d('-0.1'))
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)

        self.assertEqual(quantize(d(0.1), d('1.0')), 0)
        self.assertEqual(quantize(d(1.0), d('1.0')), 1)
        self.assertEqual(quantize(d(10.0), d('1.0')), 10)

        self.assertEqual(quantize(d(0.26), d('0.5')), 1)
        self.assertEqual(quantize(d(0.25), d('0.5')), 0)  # rounds down
        self.assertEqual(quantize(d(0.24), d('0.5')), 0)

        self.assertEqual(quantize(d(1.26), d('0.5'), rounding=Rounding.DOWN), 2)
        self.assertEqual(quantize(d(1.25), d('0.5'), rounding=Rounding.DOWN), 2)
        self.assertEqual(quantize(d(1.24), d('0.5'), rounding=Rounding.DOWN), 2)

        self.assertEqual(quantize(d(1.26), d('0.5'), rounding=Rounding.UP), 3)
        self.assertEqual(quantize(d(1.25), d('0.5'), rounding=Rounding.UP), 3)
        self.assertEqual(quantize(d(1.24), d('0.5'), rounding=Rounding.UP), 3)

        self.assertEqual(quantize(d(1.26e-9), d('0.5e-9')), 3)
        self.assertEqual(quantize(d(1.25e-9), d('0.5e-9')), 2)
        self.assertEqual(quantize(d(1.24e-9), d('0.5e-9')), 2)

    def test_scale(self):
        with self.assertRaises(ValueError) as context:
            scale(1, '0')
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)
        with self.assertRaises(ValueError) as context:
            scale(1, '-0.1')
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)

        self.assertEqual(scale(0, '1.0'), 0)
        self.assertEqual(scale(1, '1.0'), 1.0)
        self.assertEqual(scale(10, '1.0'), 10.0)

        self.assertEqual(scale(1, '0.5'), 0.5)
        self.assertEqual(scale(0, '0.5'), 0)

        self.assertEqual(scale(3, '0.5e-9'), 1.5e-9)
        self.assertEqual(scale(2, '0.5e-9'), 1.0e-9)
