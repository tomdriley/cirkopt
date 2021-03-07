import unittest

from src.netlist import Netlist, BaseNetlistFile
from src.liberty_parser import LibertyParser
from src.netlist_cost_functions import delay_cost_function, longest_delay
from tests.mock_file import MockFile
from tests.netlist_example import NETLIST_F3E7F6B4_EXAMPLES
from tests.liberty_example import LIBERTY_EXAMPLE, LIBERTY_F3E7F6B4_EXAMPLE


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
        # Parse netlists to create candidates
        netlists = list()
        for netlist_file in NETLIST_F3E7F6B4_EXAMPLES
            netlist_mock_file = MockFile()
            netlist_mock_file.write(netlist_file)
            base_netlist_file = BaseNetlistFile(netlist_mock_file)
            netlists.append(Netlist(base_netlist_file))

        # Parse ldb to create LibertyResult
        ldb_file = MockFile()
        ldb_file.write(LIBERTY_EXAMPLE)
        liberty_result = LibertyParser().parse(ldb_file)

        # Calculate worse case delays
        cost_map = delay_cost_function(
            candidates=netlists,
            simulation_result=liberty_result,
            delay_idx=(0,0),
        )

        expected_mock_file = {
            "INVX1_00": 0.00958782,
            "INVX1_01": 0.00865761,
            "INVX1_02": 0.00810281,
            "INVX1_03": 0.00776497,
            "INVX1_04": 0.007472,
            "INVX1_05": 0.00727783,
            "INVX1_06": 0.00714249,
            "INVX1_07": 0.0035648,
            "INVX1_08": ,
        }

