import unittest
import json

from src.cirkopt_json import ObjectEncoder
from src.file_io import MockFile, IFile
from src.netlist import Netlist, BaseNetlistFile

JSON_MOCK_FILE = r"""{"__MockFile__": true, "_path": "/path/to/file", "_contents": ""}"""

JSON_BASE_NETLIST_FILE = r"""{
    "__BaseNetlistFile__": true,
    "_path": "/path/to/a/different/file",
    "_contents": ""
}"""

JSON_NETLIST = r"""{
    "__Netlist__": true,
    "base_netlist_file": {
        "__BaseNetlistFile__": true,
        "_path": "",
        "_contents": ""
    },
    "cell_name": "Cell Name",
    "device_widths": [
        1,
        3.0,
        5.5
    ],
    "device_lengths": [
        0
    ],
    "device_fingers": [
        1000000000000000.0,
        1e+16,
        1e+16,
        1.11e-12,
        2e+19
    ]
}"""


class TestJSON(unittest.TestCase):
    def test_json(self):
        self.maxDiff = None

        file1: MockFile = MockFile(r"/path/to/file")
        self.assertEqual(
            json.dumps(file1, cls=ObjectEncoder),
            JSON_MOCK_FILE,
        )
        self.assertEqual(
            json.loads(JSON_MOCK_FILE, object_hook=IFile.from_json),
            file1,
        )

        file2 = MockFile(r"/path/to/a/different/file")
        base_netlist_file = BaseNetlistFile.create(file2)
        self.assertEqual(
            json.dumps(base_netlist_file, cls=ObjectEncoder, indent=4),
            JSON_BASE_NETLIST_FILE,
        )
        self.assertEqual(
            json.loads(JSON_BASE_NETLIST_FILE, object_hook=BaseNetlistFile.from_json),
            base_netlist_file,
        )

        netlist = Netlist.create(
            base_netlist_file=BaseNetlistFile.create(MockFile()),
            cell_name="Cell Name",
            device_widths=tuple([1, 3.0, 5.5]),
            device_lengths=tuple([0]),
            device_fingers=tuple([1e15, 1e16, 1.0e16, 1.110e-12, 200e17]),
        )
        self.assertEqual(
            json.dumps(netlist, cls=ObjectEncoder, indent=4),
            JSON_NETLIST,
        )
        self.assertEqual(
            json.loads(JSON_NETLIST, object_hook=Netlist.from_json), netlist
        )
