import unittest

from src.liberty_parser import LibertyParser
from tests.liberty_example import LIBERTY_EXAMPLE, LIBERTY_EXAMPLE_MORE_CELLS
from tests.mock_file import MockFile


class TestLibertyParser(unittest.TestCase):

    # pylint: disable=no-member
    def test_parsing_valid_example(self):
        mock_file = MockFile()
        mock_file.write(LIBERTY_EXAMPLE)

        parser = LibertyParser()

        root = parser.parse(mock_file)

        # Assert a handful of statments
        self.assertTrue("example_tt_1.0_70" in root.library)
        ldb = root.library["example_tt_1.0_70"]

        self.assertEqual(ldb.comment, "")
        self.assertEqual(ldb.date, "$Date: Mon Feb  1 21:38:31 2021 $")
        self.assertEqual(ldb.revision, "1.0")
        self.assertEqual(ldb.delay_model, "table_lookup")
        self.assertEqual(ldb.default_cell_leakage_power, 0)
        self.assertEqual(ldb.default_max_transition, 0.3)
        self.assertTupleEqual(ldb.capacitive_load_unit, (1, "pf"))
        self.assertTupleEqual(ldb.voltage_map, (("VDD", 1), ("VSS", 0)))

        self.assertEqual(len(ldb.operating_conditions), 1)
        self.assertTrue("tt_1.0_70" in ldb.operating_conditions)
        operating_conditions = ldb.operating_conditions["tt_1.0_70"]
        self.assertEqual(operating_conditions.process, 1)
        self.assertEqual(operating_conditions.temperature, 70)
        self.assertEqual(operating_conditions.voltage, 1)

        self.assertEqual(len(ldb.cell), 1)
        self.assertTrue("INVX1_4" in ldb.cell)
        cell = ldb.cell["INVX1_4"]

        self.assertEqual(len(cell.pin), 2)
        self.assertTrue("Y" in cell.pin)
        self.assertTrue("A" in cell.pin)
        y = cell.pin["Y"]
        a = cell.pin["A"]

        timing = y.timing
        self.assertEqual(len(timing.cell_rise), 1)
        self.assertTrue("delay_template" in timing.cell_rise)
        cell_rise = timing.cell_rise["delay_template"]
        self.assertTupleEqual(cell_rise.index_1, ((0.006, 0.3),))
        self.assertTupleEqual(cell_rise.index_2, ((0.0001, 0.07),))
        self.assertTupleEqual(
            cell_rise.values, ((0.011013, 0.366337), (0.080447, 0.540745))
        )

    def test_attribute_name_duplicated_as_group_name(self):
        mock_file = MockFile()

        file_with_attribute_duplicated_as_group_name = """
        library (bruh) {
          comment : "";
          comment (comment_as_group) {
          }
        }
        """
        mock_file.write(file_with_attribute_duplicated_as_group_name)

        parser = LibertyParser()

        with self.assertRaises(Exception) as context:
            parser.parse(mock_file)

        self.assertIn(
            "Group with group name 'comment' already defined as attribute",
            context.exception.args,
        )

    def test_group_name_duplicated_as_attribute_name(self):
        mock_file = MockFile()

        file_with_group_name_duplicated_as_attribute = """
        library (bruh) {
          comment (comment_as_group) {
          }
          comment : "";
        }
        """
        mock_file.write(file_with_group_name_duplicated_as_attribute)

        parser = LibertyParser()

        with self.assertRaises(Exception) as context:
            parser.parse(mock_file)

        self.assertIn(
            "Member name 'comment' already defined as group name",
            context.exception.args,
        )

    def test_multiple_cells(self):
        mock_file = MockFile()
        mock_file.write(LIBERTY_EXAMPLE_MORE_CELLS)

        parser = LibertyParser()

        root = parser.parse(mock_file)

        self.assertTrue("example_tt_1.0_70" in root.library)
        ldb = root.library["example_tt_1.0_70"]

        self.assertEqual(len(ldb.cell), 10)

        INVX1_8 = ldb.cell["INVX1_8"]
        self.assertEqual(INVX1_8.cell_leakage_power, 0.105498)
        self.assertEqual(INVX1_8.pin["Y"].timing.cell_fall.values[1][0], 0.0318036)
