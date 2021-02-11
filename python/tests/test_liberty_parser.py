import unittest

from src.liberty_parser import LibertyParser
from tests.libery_example import liberty_example
from tests.mock_file import MockFile


class TestLibertyParser(unittest.TestCase):

    def test_actual(self):
        mock_file = MockFile()
        mock_file.write(liberty_example)

        parser = LibertyParser()

        root = parser.parse(mock_file)[0]

        self.assertEqual(root[0], "library")
        self.assertEqual(root[1], "example_tt_1.0_70")

        self.assertEqual(root.comment, "")
        self.assertEqual(root.date, "$Date: Mon Feb  1 21:38:31 2021 $")
        self.assertEqual(root.revision, "1.0")
        self.assertEqual(root.delay_model, "table_lookup")
        self.assertEqual(root.default_cell_leakage_power, 0)
        self.assertEqual(root.default_max_transition, 0.3)

        operating_conditions = root.operating_conditions
        self.assertEqual(operating_conditions[0], "tt_1.0_70")
        self.assertEqual(operating_conditions.process, 1)
        self.assertEqual(operating_conditions.temperature, 70)
        self.assertEqual(operating_conditions.voltage, 1)