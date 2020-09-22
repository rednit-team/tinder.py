import logging
import time
from random import random

import requests

from tinder.exceptions import Unauthorized, Forbidden, NotFound, RequestFailed


class Http:
    _base_url = "https://api.gotinder.com"
    _headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) "
                      "Chrome/85.0.4183.102 Safari/537.36",
        "Content-Type": "application/json",
        "X-Auth-Token": "",
    }

    def __init__(self, auth_token: str):
        self._headers["X-Auth-Token"] = auth_token

    def get(self, route: str) -> requests.Response:
        return self._make_request("GET", route)

    def post(self, route: str, body: dict = None) -> requests.Response:
        return self._make_request("POST", route, json=body)

    def put(self, route: str, body: dict = None) -> requests.Response:
        return self._make_request("PUT", route, json=body)

    def delete(self, route: str) -> requests.Response:
        return self._make_request("DELETE", route)

    def _make_request(self, method: str, route: str, **kwargs) -> requests.Response:
        url = self._base_url + route
        logging.debug("Sending {} request to {}".format(method, url))
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
            logging.debug("Got response: {}".format(response.json()))
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
                logging.warning("Too many requests. Waiting for %f secs" % timeout)
                time.sleep(timeout)
                logging.warning("Reattempting...")
                self._make_request(method, route)
            else:
                raise RequestFailed(response)
        else:
            logging.warning("Something went wrong. Reattempting Request. Status Code %d" % status)
            self._make_request(method, route)
