__all__ = ["make"]


# Possible assessment responses
__RESPONSE_NO = "no"
__RESPONSE_MAYBE = "maybe"
__RESPONSE_YES = "yes"


def make(user_details: dict) -> str:
    url_params = {
        "latitude": user_details["lat"],
        "longitude": user_details["lng"],
        # "radius": user_details["acc"],
        "radius": 200,  # TODO Exact val TBD, see gh-7
        "categories": "restaurants,hotdogs",
        "locale": "en_US",
        "limit": 10,
        "sort_by": "rating",
        "price": "1,2,3"
    }
    return __RESPONSE_NO
