import sys
import time

from random import random

import requests

from tinder.exceptions import *


class Http:
    _base_url = "https://api.gotinder.com"
    _headers = {
        'platform': 'web',
        "User-agent": "Python/{0[0]}.{0[1]}.{0[2]} requests/{1}".format(sys.version_info, requests.__version__),
        "Accept": "application/json",
        "X-Auth-Token": ""
    }

    def __init__(self, auth_token: str):
        self._headers["X-Auth-Token"] = auth_token

    def get(self, route: str) -> requests.Response:
        return self._make_request("GET", route)

    def post(self, route: str, body: dict = None) -> requests.Response:
        return self._make_request("POST", route, body=body)

    def put(self, route: str, body: dict = None) -> requests.Response:
        return self._make_request("PUT", route, body=body)

    def delete(self, route: str) -> requests.Response:
        return self._make_request("DELETE", route)

    def fix(self):
        data = {"message": "Test"}
        self._make_request("POST", "/like/5f5fa4e88a49eb010099be13")

    def _make_request(self, method: str, route: str, **kwargs) -> requests.Response:
        url = self._base_url + route
        print("Sending {} request to {}".format(method, url))
        if method == "GET":
            response = requests.get(url, headers=self._headers)
        elif method == "POST":
            response = requests.post(url, headers=self._headers, **kwargs)
        elif method == "PUT":
            response = requests.put(url, headers=self._headers, **kwargs)
        elif method == "DELETE":
            response = requests.delete(url, headers=self._headers)
        else:
            raise ValueError("Invalid request method!")

        status = response.status_code
        if 200 <= status < 300:
            print("Got response:", response.json())
            return response
        elif 400 <= status < 500:
            if status == 401:
                raise Unauthorized(response)

            elif status == 403:
                raise Forbidden(response)

            elif status == 404:
                raise NotFound(response)

            elif status == 429:
                timeout = 5 * random()
                print("Too many requests. Waiting for %f secs" % timeout)
                time.sleep(timeout)
                print("Reattempting...")
                self._make_request(method, route)
            else:
                raise RequestFailed(response)
        else:
            print("Something went wrong. Reattempting Request. Status Code", status)
            self._make_request(method, route)
