import json
from pymodules.logger import logger
from pymodules.http_requests import APICaller
from pymodules import constant
from pymodules.constant import NASA_FIREBALL_BASE_URL


class NasaFireballAPI(object):
    """
    Fireball API
    """
    url = NASA_FIREBALL_BASE_URL
    data = None

    def __init__(self):
        self.dbapi = APICaller(self.url)

    def fetch_all_data(self):
        endpoint = "fireball.api"
        status, response = self.dbapi.call_api(
            endpoint, "GET", auth=None, max_attempt=constant.FIREBALL_API_MAX_ATTEMPT
        )

        res = None
        if status == 200:
            res = json.loads(response.content)
        else:
            logger.warn(
                "Could,n't get data from endpoint {}, get_all_fireball_data returned status - {}".format(
                    endpoint, status
                )
            )
        return status, res

    def fetch_most_recent_data(self, count):
        endpoint = "fireball.api?limit = {count_of_records}".format(
            count_of_records=count
        )
        status, response = self.dbapi.call_api(
            endpoint, "GET", auth=None, max_attempt=constant.FIREBALL_API_MAX_ATTEMPT
        )

        res = None
        if status == 200:
            res = json.loads(response.content)
        else:
            logger.warn(
                "Could,n't get data from endpoint {}, get_all_fireball_data returned status - {}".format(
                    endpoint, status
                )
            )
        return status, res

    def fetch_data_by_altitude(self, date_min, req_alt=True):
        endpoint = "fireball.api?date-min={date}&req-alt={req_alt}".format(
            date=date_min,
            req_alt=req_alt
        )
        status, response = self.dbapi.call_api(
            endpoint, "GET", auth=None, max_attempt=constant.FIREBALL_API_MAX_ATTEMPT
        )

        res = None
        if status == 200:
            res = json.loads(response.content)
        else:
            logger.warn(
                "Could,n't get data from endpoint {}, get_all_fireball_data returned status - {}".format(
                    endpoint, status
                )
            )
        return status, res

    def fetch_data_by_location(self, date_min, req_loc=False):
        """
        Fetch data from NASA API
        :param date_min:
        :param req_loc:
        :return:
        """
        endpoint = "fireball.api?date-min={date}&req-loc={req_loc}".format(
            date=date_min,
            req_loc=req_loc
        )
        status, response = self.dbapi.call_api(
            endpoint, "GET", auth=None, max_attempt=constant.FIREBALL_API_MAX_ATTEMPT
        )

        res = None
        assert int(status) == 200, "API respond status code {}. Something went wrong while fetching data by location".format(status)

        res = json.loads(response.content)
        if res != [] and res != {}:
            try:
                assert (res.get('signature',None) == constant.FIREBALL_RESPONSE_SIGNATURE_MAP), "SIGNATURE IS NOT MATCHING"
                assert (int(res.get('count', 0)) > 0), "API could not find data matching criteria"
                return status, res
            except Exception as e:
                raise Exception("Issue with Signature or count in API response, Exception: {} ".format(e))
        else:
            logger.warn("Found no records in response content body")