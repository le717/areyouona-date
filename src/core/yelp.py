import os
import json

import requests


__all__ = ["Yelp"]


class Yelp:

    def __init__(self):
        self.__API_KEY = None
        self.__request_url = "https://api.yelp.com/v3/businesses/search"
        self.__request_file = ".data/yelp-requests.json"
        self.__request_limits = self.__get_request_limits()

    def __get_request_limits(self) -> dict:
        if not os.path.exists(self.__request_file):
            return {}

        with open(self.__request_file, "rt") as f:
            return json.loads(f.read())

    def __set_request_limits(self, data: dict) -> dict:
        request_limits = {
            "RateLimit-DailyLimit": data["RateLimit-DailyLimit"],
            "RateLimit-Remaining": data["RateLimit-Remaining"],
            "RateLimit-ResetTime": data["RateLimit-ResetTime"],
        }

        self.__request_limits = request_limits
        with open(self.__request_file, "wt") as f:
            f.write(json.dumps(request_limits))

    def init_app(self, app):
        self.__API_KEY = app.config.get("YELP_API_KEY")

        # The Yelp API key is missing
        error_msg = (
            "A Yelp API key is required. "
            "Get one at https://www.yelp.com/developers."
        )
        if self.__API_KEY is None:
            raise KeyError(error_msg)

    def make_request(self, url_params: dict) -> dict:
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
        return {"total": 0}

    def make_cached_request(self, url_params: dict) -> list:
        print("**** `make_cached_request` is only for development use! ****")

        if os.path.exists("data.json"):
            print("Returning cached data")
            with open("data.json", "rt") as f:
                data = f.read()
            return json.loads(data)

        data = self.make_request(url_params)
        with open("data.json", "wt") as f:
            f.write(json.dumps(data, indent=2))
        return data
