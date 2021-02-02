import unittest
import textwrap

from netlist import BaseNetlistFile, Netlist
from tests.mock_file import MockFile


TEST_NETLIST = """
** Library name: gsclib045
** Cell name: INVX1_3
** View name: schematic
.subckt INVX1_3 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=45e-9 W=250e-9 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=50e-9 W=300e-9 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=2
.ends INVX1_3
"""


class TestNetlist(unittest.TestCase):

    def test_base_netlist_file(self):
        mock_file = MockFile()
        mock_file.write("some content")

        netflist_file = BaseNetlistFile(mock_file)
        self.assertEqual("some content", netflist_file.contents())

    def test_read_netlist_values(self):
        mock_file = MockFile()
        mock_file.write(TEST_NETLIST)

        netflist_file = BaseNetlistFile(mock_file)
        netlist = Netlist(netflist_file)

        self.assertEqual(netlist.cell_name, "INVX1_3")
        self.assertEqual(netlist.device_widths, (250e-9, 300e-9))
        self.assertEqual(netlist.device_lengths, (45e-9, 50e-9))
        self.assertEqual(netlist.device_fingers, (1, 2))

    def test_write_netlist_values(self):
        mock_file = MockFile()
        mock_file.write(TEST_NETLIST)

        netflist_file = BaseNetlistFile(mock_file)
        netlist = Netlist(netflist_file)

        new_netlist = netlist.mutate(
            device_widths=(260e-9, 310e-9),
            device_lengths=(50e-9, 60e-9),
            device_fingers=(2, 3)
        )

        new_mock_file = MockFile()
        new_netlist.persist(new_mock_file)

        expected_netlist_string = """
            ** Library name: gsclib045
            ** Cell name: INVX1_3
            ** View name: schematic
            .subckt INVX1_3 A Y VDD VSS
            *.PININFO  VSS:I VDD:I A:I Y:O
            ** Above line required by Conformal LEC - DO NOT DELETE
    
            mp0 Y A VDD VDD g45p1svt L=5e-08 W=2.6e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=2
            mn0 Y A VSS VSS g45n1svt L=6e-08 W=3.1e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=3
            .ends INVX1_3
            """

        self.assertEqual(
            new_mock_file.read(),
            textwrap.dedent(expected_netlist_string)
        )
