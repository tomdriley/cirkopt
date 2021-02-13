import unittest

from src.liberty_parser import LibertyParser
from tests.liberty_example import LIBERTY_EXAMPLE
from tests.mock_file import MockFile


class TestLibertyParser(unittest.TestCase):

    def test_actual(self):
        mock_file = MockFile()
        mock_file.write(LIBERTY_EXAMPLE)

        parser = LibertyParser()

        root = parser.parse(mock_file)

        # Assert a handful of statments
        self.assertEqual(root.group_name, "library")
        self.assertEqual(root.name, "example_tt_1.0_70")

        self.assertEqual(root.comment, "")
        self.assertEqual(root.date, "$Date: Mon Feb  1 21:38:31 2021 $")
        self.assertEqual(root.revision, "1.0")
        self.assertEqual(root.delay_model, "table_lookup")
        self.assertEqual(root.default_cell_leakage_power, 0)
        self.assertEqual(root.default_max_transition, 0.3)
        self.assertListEqual(root.capacitive_load_unit, [1, "pf"])

        self.assertEqual(len(root.operating_conditions), 1)
        operating_conditions = root.operating_conditions[0]
        self.assertEqual(operating_conditions.group_name, "operating_conditions")
        self.assertEqual(operating_conditions.name, "tt_1.0_70")
        self.assertEqual(operating_conditions.process, 1)
        self.assertEqual(operating_conditions.temperature, 70)
        self.assertEqual(operating_conditions.voltage, 1)

        self.assertEqual(len(root.cell), 1)
        cell = root.cell[0]
        self.assertEqual(cell.group_name, "cell")
        self.assertEqual(cell.name, "INVX1_4")

        self.assertEqual(len(cell.pin), 2)
        y = cell.pin[0]
        self.assertEqual(y.group_name, "pin")
        self.assertEqual(y.name, "Y")

        self.assertEqual(len(y.timing), 1)
        timing = y.timing[0]
        self.assertEqual(timing.group_name, "timing")
        self.assertEqual(timing.name, "")

        self.assertEqual(len(timing.cell_rise), 1)
        cell_rise = timing.cell_rise[0]
        self.assertEqual(cell_rise.group_name, "cell_rise")
        self.assertEqual(cell_rise.name, "delay_template")
        self.assertEqual(cell_rise.index_1, [[0.006, 0.3]])
        self.assertEqual(cell_rise.index_2, [[0.0001, 0.07]])
        self.assertEqual(cell_rise.values, [[0.011013, 0.366337], [0.080447, 0.540745]])
