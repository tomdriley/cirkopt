import unittest

from src.fixed_point import fixed, floating


class TestFixedPoint(unittest.TestCase):

    def test_fixed(self):
        with self.assertRaises(Exception) as context:
            fixed(1.0, 0)
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)
        with self.assertRaises(Exception) as context:
            fixed(1.0, -0.1)
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)

        self.assertEqual(fixed(0.1, 1.0), 0)
        self.assertEqual(fixed(1.0, 1.0), 1)
        self.assertEqual(fixed(10.0, 1.0), 10)

        self.assertEqual(fixed(0.26, 0.5), 1)
        self.assertEqual(fixed(0.25, 0.5), 0)  # rounds down
        self.assertEqual(fixed(0.24, 0.5), 0)

        self.assertEqual(fixed(1.26e-9, 0.5e-9), 3)
        self.assertEqual(fixed(1.25e-9, 0.5e-9), 2)
        self.assertEqual(fixed(1.24e-9, 0.5e-9), 2)

    def test_floating(self):
        with self.assertRaises(Exception) as context:
            floating(1, 0)
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)
        with self.assertRaises(Exception) as context:
            floating(1, -0.1)
            self.assertIn("Precision cannot be less than or equal to 0", context.exception.args)

        self.assertEqual(floating(0, 1.0), 0)
        self.assertEqual(floating(1, 1.0), 1.0)
        self.assertEqual(floating(10, 1.0), 10.0)

        self.assertEqual(floating(1, 0.5), 0.5)
        self.assertEqual(floating(0, 0.5), 0)

        # need almost equals since value cannot be represented as binary fractions
        # https://docs.python.org/3/tutorial/floatingpoint.html
        self.assertAlmostEqual(floating(3, 0.5e-9), 1.5e-9, places=9)
        self.assertAlmostEqual(floating(2, 0.5e-9), 1.0e-9, places=9)
