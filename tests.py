import unittest

from guolei_py3_hikvision.isc import Api as HikvisionIscApi


class HikvisionISCTestCase(unittest.TestCase):
    def test_something(self):
        hikvision_isc_api = HikvisionIscApi(
            host="https://60.22.91.250:1443",
            ak="20552343",
            sk="4h9rlhpPLRmjW0pTuow1"
        )
        print(
            hikvision_isc_api.api_resource_v1_card_cardList(
                requests_request_kwargs_json={
                    "pageNo":1,
                    "pageSize":10,
                }
            )
        )
        self.assertTrue(True, "Test Failed")  # add assertion here


if __name__ == '__main__':
    unittest.main()
