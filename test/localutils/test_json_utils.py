import unittest
from datetime import datetime, timezone

import src.localutils.json_utils as ju


class MyTestCase(unittest.TestCase):
    def test_json_from_py(self):
        dt = datetime(2024, 5, 16, 22, 0, tzinfo=timezone.utc)
        json_str = ju.json_from_py(dt)
        self.assertEqual(r'"2024-05-16T22:00:00+00:00"', json_str)


if __name__ == '__main__':
    unittest.main()
