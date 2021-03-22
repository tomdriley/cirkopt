import unittest
import textwrap
from dataclasses import FrozenInstanceError

from src.netlist import BaseNetlistFile, Netlist
from src.file_io import MockFile
from tests.netlist_example import TEST_NETLIST


class TestNetlist(unittest.TestCase):
    def test_base_netlist_file(self):
        mock_file = MockFile()
        mock_file.write("some content")

        netflist_file = BaseNetlistFile.create(mock_file)
        self.assertEqual("some content", netflist_file.contents())

    def test_read_netlist_values(self):
        mock_file = MockFile()
        mock_file.write(TEST_NETLIST)

        netflist_file = BaseNetlistFile.create(mock_file)
        netlist = Netlist.create(netflist_file)

        self.assertEqual(netlist.cell_name, "INVX1_3")
        self.assertEqual(netlist.device_widths, (250e-9, 300e-9))
        self.assertEqual(netlist.device_lengths, (45e-9, 50e-9))
        self.assertEqual(netlist.device_fingers, (1, 2))

    def test_write_netlist_values(self):
        mock_file = MockFile()
        mock_file.write(TEST_NETLIST)

        netflist_file = BaseNetlistFile.create(mock_file)
        netlist = Netlist.create(netflist_file)

        new_netlist = netlist.clone(
            cell_name="INVX1_4",
            device_widths=(260e-9, 310e-9),
            device_lengths=(50e-9, 60e-9),
            device_fingers=(2, 3),
        )

        new_mock_file = MockFile()
        new_netlist.persist(new_mock_file)

        expected_netlist_string = """
            ** Library name: gsclib045
            ** Cell name: INVX1_4
            ** View name: schematic
            .subckt INVX1_4 A Y VDD VSS
            *.PININFO  VSS:I VDD:I A:I Y:O
            ** Above line required by Conformal LEC - DO NOT DELETE
    
            mp0 Y A VDD VDD g45p1svt L=5e-08 W=2.6e-07 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=2
            mn0 Y A VSS VSS g45n1svt L=6e-08 W=3.1e-07 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=3
            .ends INVX1_4
            """

        self.assertEqual(new_mock_file.read(), textwrap.dedent(expected_netlist_string))

    def test_eq_hash(self):
        file1: MockFile = MockFile("/some/path", "Some Content.")
        file2: MockFile = MockFile("/some/path", "Some Content.")
        bnf1: BaseNetlistFile = BaseNetlistFile.create(file1)
        bnf2: BaseNetlistFile = BaseNetlistFile.create(file2)

        self.assertEqual(bnf1, bnf2)
        self.assertEqual(hash(bnf1), hash(bnf2))

        with self.assertRaises(FrozenInstanceError):
            bnf1._path = "/different/path"  # pylint: disable=protected-access

        file1.write(TEST_NETLIST)
        file2.write(TEST_NETLIST)

        bnf3: BaseNetlistFile = BaseNetlistFile.create(file1)
        bnf4: BaseNetlistFile = BaseNetlistFile.create(file2)

        self.assertNotEqual(bnf1, bnf3)
        self.assertNotEqual(hash(bnf1), hash(bnf3))

        nl1: Netlist = Netlist.create(bnf3)
        nl2: Netlist = Netlist.create(bnf4)

        self.assertEqual(nl1, nl2)
        self.assertEqual(hash(nl1), hash(nl2))

        with self.assertRaises(FrozenInstanceError):
            nl1.base_netlist_file = bnf1

        # Changing name doesn't matter for equality and hash
        nl3: Netlist = Netlist.create(bnf3, "Cell Name")
        self.assertEqual(nl1, nl3)
        self.assertEqual(hash(nl1), hash(nl3))

        # Hash and eq depend on device params and base netlist file
        nl3: Netlist = Netlist.create(bnf3, device_widths=(123e-9, 123-9))
        self.assertNotEqual(nl1, nl3)
        self.assertNotEqual(hash(nl1), hash(nl3))

