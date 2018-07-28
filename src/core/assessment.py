__all__ = ["make"]


# Possible assessment responses
__RESPONSE_NO = "no"
__RESPONSE_MAYBE = "maybe"
__RESPONSE_YES = "yes"


def make(user_details: dict) -> str:
    # Construct the required request parameters
    url_params = {
        "latitude": user_details["lat"],
        "longitude": user_details["lng"],
        "radius": math.ceil(user_details["acc"]),
        "categories": "restaurants,hotdogs",
        "locale": "en_US",
        "limit": 10,
        "sort_by": "rating",
        "price": "1,2,3"
    }
    return __RESPONSE_NO
