import unittest
from datetime import datetime, timedelta
import src.aws_cost_explorer.localutils.date_utils as du


#TODO move to general date utils class
class MyTestCase(unittest.TestCase):
    def test_date_round_seconds(self):
        dt = datetime.fromisoformat("2024-01-01T08:00:01.001")
        expected_round_down = dt = datetime.fromisoformat("2024-01-01:08:00:01")
        self.assertEqual(expected_round_down, du.date_round_seconds(dt))
        self.assertEqual(expected_round_down, du.date_round_seconds(dt,round_down=True))
        dt = datetime.fromisoformat("2024-01-01T08:00:01.501")
        self.assertEqual(expected_round_down + timedelta(seconds=1), du.date_round_seconds(dt))
        self.assertEqual(expected_round_down, du.date_round_seconds(dt, round_down=True))


if __name__ == '__main__':
    unittest.main()

