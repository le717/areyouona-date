import os
import json

import requests


__all__ = ["Yelp"]


class Yelp:

    def __init__(self):
        self.__API_KEY = None
        self.request_url = "https://api.yelp.com/v3/businesses/search"

    def init_app(self, app):
        self.__API_KEY = app.config.get("YELP_API_KEY")

        # The Yelp API key is missing
        error_msg = (
            "A Yelp API key is required. "
            "Get one at https://www.yelp.com/developers."
        )
        if self.__API_KEY is None:
            raise KeyError(error_msg)

    def make_request(self, url_params: dict) -> list:
        headers = {
            "Authorization": f"Bearer {self.__API_KEY}"
        }
        r = requests.get(
            self.request_url,
            headers=headers,
            params=url_params
        )

        # The request was successful
        if r.status_code == requests.codes.ok:
            return r.json()
        return []

    def make_cached_request(self, url_params: dict) -> list:
        print("***** `make_cached_request` is only for development use! *****")

        if os.path.isfile("data.json"):
            with open("data.json", "rt") as f:
                data = f.read()
            return json.loads(data)

        data = self.make_request(url_params)
        with open("data.json", "wt") as f:
            f.write(json.dumps(data))
        return data