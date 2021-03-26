import unittest

from src.liberty_parser import LibertyParser
from src.file_io import MockFile
from src.exceptions import CirkoptException
from tests.liberty_example import LIBERTY_EXAMPLE


class TestLibertyParser(unittest.TestCase):

    # pylint: disable=no-member
    def test_parsing_valid_example(self):
        mock_file = MockFile()
        mock_file.write(LIBERTY_EXAMPLE)

        parser = LibertyParser()

        root = parser.parse(mock_file)

        # Assert a handful of statments
        self.assertEqual(root.group_name, "library")
        self.assertEqual(root.name, "example_tt_1.0_70")

        self.assertEqual(root.comment, "")
        self.assertEqual(root.date, "$Date: Sun Feb 14 11:55:04 2021 $")
        self.assertEqual(root.revision, "1.0")
        self.assertEqual(root.delay_model, "table_lookup")
        self.assertEqual(root.default_cell_leakage_power, 0)
        self.assertEqual(root.default_max_transition, 0.3)
        self.assertTupleEqual(root.capacitive_load_unit, (1, "pf"))
        self.assertTupleEqual(root.voltage_map, (("VDD", 1), ("VSS", 0)))

        self.assertEqual(len(root.operating_conditions), 1)
        operating_conditions = root.operating_conditions[0]
        self.assertEqual(operating_conditions.group_name, "operating_conditions")
        self.assertEqual(operating_conditions.name, "tt_1.0_70")
        self.assertEqual(operating_conditions.process, 1)
        self.assertEqual(operating_conditions.temperature, 70)
        self.assertEqual(operating_conditions.voltage, 1)

        expected_cell_rise_values = (
            ((0.00832102, 0.489515), (0.0672285, 0.668921)),
            ((0.0102831, 0.887086), (0.0790586, 1.06402)),
            ((0.00935542, 0.626023), (0.0733304, 0.803784)),
            ((0.00880019, 0.478776), (0.0711915, 0.658158)),
            ((0.00846291, 0.388352), (0.0696257, 0.567804)),
            ((0.00817958, 0.32283), (0.0672366, 0.501756)),
            ((0.00796714, 0.276713), (0.0654463, 0.456428)),
            ((0.00782771, 0.242445), (0.0640842, 0.421923)),
            ((0.00774737, 0.216002), (0.0632206, 0.396036)),
            ((0.00769541, 0.194961), (0.0625122, 0.375119)),
        )
        self.assertEqual(len(root.cell), 10)
        for idx, cell in enumerate(root.cell):
            self.assertEqual(cell.group_name, "cell")
            self.assertEqual(cell.name, f"INVX1_{idx+1}")

            self.assertEqual(len(cell.pin), 2)
            y = cell.pin[0]
            self.assertEqual(y.group_name, "pin")
            self.assertEqual(y.name, "Y")
            self.assertEqual(y.direction, "output")
            a = cell.pin[1]
            self.assertEqual(a.group_name, "pin")
            self.assertEqual(a.name, "A")
            self.assertEqual(a.direction, "input")

            self.assertEqual(len(y.timing), 1)
            timing = y.timing[0]
            self.assertEqual(timing.group_name, "timing")
            self.assertEqual(timing.name, "")

            self.assertFalse(hasattr(a, "timing"))

            self.assertEqual(len(timing.cell_rise), 1)
            cell_rise = timing.cell_rise[0]
            self.assertEqual(cell_rise.group_name, "cell_rise")
            self.assertEqual(cell_rise.name, "delay_template")
            self.assertTupleEqual(cell_rise.index_1, ((0.006, 0.3),))
            self.assertTupleEqual(cell_rise.index_2, ((0.0001, 0.07),))
            self.assertTupleEqual(cell_rise.values, expected_cell_rise_values[idx])

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

        with self.assertRaises(CirkoptException) as context:
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

        with self.assertRaises(CirkoptException) as context:
            parser.parse(mock_file)

        self.assertIn(
            "Member name 'comment' already defined as group name",
            context.exception.args,
        )
