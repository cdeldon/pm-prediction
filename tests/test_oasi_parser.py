import os
import unittest

import pm


class OasiParserTest(unittest.TestCase):
    def setUp(self):
        self.json_data = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      "test_oasi_parser_data.json")

    def test_oasi_can_build(self) -> None:
        try:
            _ = pm.oasi.Settings(self.json_data)
        except RuntimeError:
            self.fail("Could not build Oasi Settings object")


if __name__ == '__main__':
    unittest.main()
