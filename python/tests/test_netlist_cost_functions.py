import unittest

from src.liberty_parser import LibertyParser
from src.netlist_cost_functions import delay_cost_function, longest_delay
from tests.liberty_example import LIBERTY_EXAMPLE
from tests.mock_file import MockFile


class TestDelayCostFunction(unittest.TestCase):
    def test_longest_delay(self):
        # Parse ldb to create LibertyResult
        mock_file = MockFile()
        mock_file.write(LIBERTY_EXAMPLE)
        liberty_result = LibertyParser().parse(mock_file)

        cells = {cell.name: cell for cell in liberty_result.cell}

        delay1_00 = longest_delay(cell=cells["INVX1_1"], delay_idx=(0, 0))
        self.assertEqual(delay1_00, 0.00832102)
        delay1_11 = longest_delay(cell=cells["INVX1_1"], delay_idx=(1, 1))
        self.assertEqual(delay1_11, 0.668921)
        delay5_01 = longest_delay(cell=cells["INVX1_5"], delay_idx=(0, 1))
        self.assertEqual(delay5_01, 0.388352)

    def test_delay_cost_function(self):
        # Parse ldb to create LibertyResult
        mock_file = MockFile()
        mock_file.write(LIBERTY_EXAMPLE)
        liberty_result = LibertyParser().parse(mock_file)

        # Calculate worse case delays
        # TODO
