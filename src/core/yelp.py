import os
import json

import requests


__all__ = ["Yelp"]


class Yelp:

    def __init__(self):
        self.__app = None
        self.__API_KEY = None
        self.__request_url = "https://api.yelp.com/v3/businesses/search"
        self.__request_file = os.path.abspath(
            os.path.join("data", "yelp-requests.json")
        )
        self.__request_limits = self.__get_request_limits()

    def __get_request_limits(self) -> dict:
        if not os.path.exists(self.__request_file):
            return {}

        with open(self.__request_file, "rt") as f:
            return json.loads(f.read())

    def __set_request_limits(self, data: dict):
        request_limits = {
            "RateLimit-DailyLimit": int(data["RateLimit-DailyLimit"]),
            "RateLimit-Remaining": int(data["RateLimit-Remaining"]),
            "RateLimit-ResetTime": data["RateLimit-ResetTime"],
        }

        self.__request_limits = request_limits
        with open(self.__request_file, "wt") as f:
            f.write(json.dumps(request_limits))

    def init_app(self, app):
        if self.__app is None:
            self.__app = app
        self.__API_KEY = app.config.get("YELP_API_KEY")
        self.__request_file = os.path.join(
            self.__app.config["APP_ROOT"],
            self.__request_file
        )

        # The Yelp API key is missing
        error_msg = (
            "A Yelp API key is required. "
            "Get one at https://www.yelp.com/developers."
        )
        if self.__API_KEY is None:
            raise KeyError(error_msg)

    def make_request(self, url_params: dict) -> dict:
        no_request_response = {"total": 0}

        # We have hit our request limit, no dates for anyone
        if self.__request_limits.get("RateLimit-Remaining", 1) == 0:
            return no_request_response

        # Authenticate with the API as documented when making a request
        # https://www.yelp.com/developers/documentation/v3/authentication
        headers = {
            "Authorization": f"Bearer {self.__API_KEY}"
        }
        r = requests.get(
            self.__request_url,
            headers=headers,
            params=url_params
        )
        self.__set_request_limits(r.headers)

        # The request was successful
        if r.status_code == requests.codes.ok:
            return r.json()
        return no_request_response
