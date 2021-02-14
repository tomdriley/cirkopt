import unittest
import src.liberate as liberate


class TestLiberate(unittest.TestCase):
    def test_error_checking(self):
        with self.assertRaises(TypeError):
            liberate.run_liberate(char_tcl_path="/does/not/exist")
        with self.assertRaises(TypeError):
            liberate.run_liberate(liberate_cmd="/does/not/exist")
