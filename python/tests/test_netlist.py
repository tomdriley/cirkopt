import unittest

from netlist import BaseNetlistFile
from tests.mock_file import MockFile


class TestNetlist(unittest.TestCase):

    def test_base_netlist_file(self):
        mock_file = MockFile()
        mock_file.write("some content")

        netflist_file = BaseNetlistFile(mock_file)
        self.assertEqual("some content", netflist_file.contents())
