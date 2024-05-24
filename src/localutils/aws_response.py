from typing import TypeVar
from datetime import datetime as dt


class AwsResponse:
    def __init__(self, boto_result: dict):
        self.complete_result = boto_result
        self.response_meta = boto_result['ResponseMetadata']


#CEResultList = TypeVar("CEResultList", bound="list[CEResultByTime]")
type CEResultList = list[CEResultByTime]


class AwsCostExplorerResponse(AwsResponse):

    COST_METRIC_BLENDED_COST = "BlendedCost"

    def __init__(self, boto_result: dict):
        super().__init__(boto_result)
        self.result_by_time: [dict] = self.complete_result['ResultsByTime']
        self.result_by_time_list:CEResultList = CEResultByTime.from_list(self.result_by_time)

    def get_result_list(self) -> CEResultList:
        return self.result_by_time_list



class CEResultByTime:
    def __init__(self, rbt: dict):
        self.start_date = dt.fromisoformat(rbt['TimePeriod']['Start'])
        self.end_date = dt.fromisoformat(rbt['TimePeriod']['End'])
        self.cost_metric = 'BlendedCost'
        self.estimated: bool = rbt['Estimated']
        self.cost: float = float(rbt['Total']['BlendedCost']['Amount'])

    @staticmethod
    def from_list(rbts: list[dict]) -> CEResultList:
        out: [CEResultByTime] = []
        for rbt in rbts:
            out.append(CEResultByTime(rbt))
        return out

    # todo ignore unit=usdo
    """ 
  {'Estimated': True,
                    'Groups': [],
                    'TimePeriod': {'End': '2024-05-22T05:00:00Z',
                                   'Start': '2024-05-22T04:00:00Z'},
                    'Total': {'BlendedCost': {'Amount': '46.3947563312',
                                              'Unit': 'USD'}}},
                                              """
