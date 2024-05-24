import unittest
from datetime import datetime, timezone

from src.localutils.aws_response import AwsCostExplorerResponse


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_input_1: dict = load_mock1()

    def test_something(self):
        r: AwsCostExplorerResponse = AwsCostExplorerResponse(self.mock_input_1)
        # for x in r.result_by_time_list:
        #    print(x)
        self.assertEqual(2, len(r.result_by_time_list))
        first_res = r.result_by_time_list[0]
        self.assertEqual(6.7114600162, first_res.cost)
        self.assertEqual(AwsCostExplorerResponse.COST_METRIC_BLENDED_COST, first_res.cost_metric)
        self.assertEqual(datetime(2024, 5, 16, 22, 0, tzinfo=timezone.utc), first_res.start_date)
        self.assertEqual(datetime(2024, 5, 16, 23, 0, tzinfo=timezone.utc), first_res.end_date)


if __name__ == '__main__':
    unittest.main()


def load_mock1():
    return {'DimensionValueAttributes': [],
            'ResponseMetadata': {'HTTPHeaders': {'cache-control': 'no-cache',
                                                 'connection': 'keep-alive',
                                                 'content-length': '28373',
                                                 'content-type': 'application/x-amz-json-1.1',
                                                 'date': 'Thu, 23 May 2024 22:16:59 GMT',
                                                 'x-amzn-requestid': 'e913e3da-22e6-4e02-8cc2-d88e541d8bb5'},
                                 'HTTPStatusCode': 200,
                                 'RequestId': 'e913e3da-22e6-4e02-8cc2-d88e541d8bb5',
                                 'RetryAttempts': 0},
            'ResultsByTime': [{'Estimated': True,
                               'Groups': [],
                               'TimePeriod': {'End': '2024-05-16T23:00:00Z',
                                              'Start': '2024-05-16T22:00:00Z'},
                               'Total': {'BlendedCost': {'Amount': '6.7114600162',
                                                         'Unit': 'USD'}}},
                              {'Estimated': True,
                               'Groups': [],
                               'TimePeriod': {'End': '2024-05-17T00:00:00Z',
                                              'Start': '2024-05-16T23:00:00Z'},
                               'Total': {'BlendedCost': {'Amount': '6.7115154337',
                                                         'Unit': 'USD'}}}
                              ]}
