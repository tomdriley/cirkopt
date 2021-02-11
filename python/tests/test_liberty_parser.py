import unittest

from src.liberty_parser import LibertyParser
from tests.libery_example import liberty_example
from tests.mock_file import MockFile


class TestLibertyParser(unittest.TestCase):

    def test_actual(self):
        mock_file = MockFile()
        mock_file.write(liberty_example)

        parser = LibertyParser()

        results = parser.parse(mock_file)

        results.pprint()
