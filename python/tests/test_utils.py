import unittest

from src.utils import single, chunked
from src.exceptions import CirkoptException


class TestUtils(unittest.TestCase):

    def test_single(self):
        with self.assertRaises(CirkoptException) as context:
            single(lambda it: True, [])
        self.assertIn("Zero items in sequence match predicate", context.exception.args)

        with self.assertRaises(CirkoptException) as context:
            single(lambda it: True, [0, 0])
        self.assertIn("More than one item in sequence matches predicate", context.exception.args)

        self.assertEqual(single(lambda it: it == 0, range(10)), 0)

    def test_chunked(self):
        # even split
        self.assertListEqual(
            list(chunked(range(10), 2)),
            [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
        )

        # uneven split
        self.assertTupleEqual(
            tuple(chunked(range(9), 2)),
            ((0, 1), (2, 3), (4, 5), (6, 7), (8, ))
        )
