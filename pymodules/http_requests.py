import requests
import json

from pymodules.logger import logger


class APICaller(object):
    """
    Core class for handling REST API Calls
    """
    DEFAULT_HEADERS = {'content-type': 'application/json','Accept': '*/*'}

    def __init__(self, base_url = None):
        self.base_url = '' if not base_url else base_url

    # TODO: IF AUTHENTINCATION IS REQUIRED
    def get_auth(self):
        pass

    def get_api_url(self, api_endpoint):
        if self.base_url:
            return '{bu}{sep}{ep}'.format(bu=self.base_url,
                                          sep='/' if not self.base_url.endswith('/') else '', ep=api_endpoint)
        else:
            return api_endpoint

    def call_api(self, api_endpoint, req_type, data=None, file_path=None, headers=None, auth=None, **kwargs):
        headers = headers if headers else self.DEFAULT_HEADERS.copy()
        api_url = self.get_api_url(api_endpoint)
        exec_attempt = 1l

        max_attempt = kwargs.pop('max_attempt', 1)
        response = None
        if data and headers.get('Content-type') == 'application/json':
            logger.info("Input Data for API Call: {}".format(data))
            data = json.dumps(data)

        cookies = auth_obj = None
        exception_list = {}
        while exec_attempt <= max_attempt:
            try:
                logger.info('Attempt {} of {} to call api - {}'.format(exec_attempt,max_attempt,api_url))
                if req_type == 'GET':
                    response = requests.get(api_url, data=data, headers=headers, auth=auth_obj, cookies = cookies,
                                            **kwargs)
                elif req_type == 'POST': #TODO: for future
                    pass
                else:
                    raise TypeError('Unknown API HTTP request type')
            except Exception as e:
                exception_list[exec_attempt] = e
                logger.error("Error occured while calling API, exception: {}".format(e))
                exec_attempt += 1
                continue
            break
        if exec_attempt > max_attempt:
            raise Exception("Max attempt {} reached while call API, Exception: {}".format(max_attempt, exception_list))

        return response.status_code, response
