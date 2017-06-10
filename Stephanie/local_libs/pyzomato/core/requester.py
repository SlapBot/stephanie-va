import requests
from Stephanie.local_libs.pyzomato.core.endpoint_manager import EndpointManager


class Requester(EndpointManager):
    def __init__(self, API_KEY=""):
        super().__init__()
        self.API_KEY = API_KEY
        self.headers = {'user-key': self.API_KEY}
        self.r = object

    def request(self, endpoint_name=None, endpoint_format=None, payload=None, raw=False, raw_url=None):
        if payload is None:
            payload = {}
        if endpoint_format:
            raw_url = self.endpoints[endpoint_name]
            if isinstance(endpoint_format, str):
                url = raw_url.format(endpoint_format)
            else:
                url = raw_url.format(*endpoint_format)
        elif raw_url:
            url = raw_url
        else:
            url = self.endpoints[endpoint_name]
        self.r = requests.get(url, params=payload, headers=self.headers)
        # self.check_for_exceptions(self.r)
        if raw:
            return self.r
        return self.r.json()

    @staticmethod
    def check_for_exceptions(request):
        status_code = request.status_code
        if status_code != 200:
            raise ConnectionError("The website couldn't be retrieved.")
