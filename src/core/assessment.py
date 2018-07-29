__all__ = ["make"]


# Common values used in making an assessment
__RESPONSE_NO = "no"
__RESPONSE_MAYBE = "maybe"
__RESPONSE_YES = "yes"
__ABSURD_ACCURACY_THRESHOLD = 1000


def make(user_details: dict) -> str:
    # The Geolocation API did not respond with good data
    # (aka an absurd accuracy meter distance) so we can't use that data
    # https://developer.mozilla.org/en-US/docs/Web/API/Coordinates)
    if user_details["acc"] >= __ABSURD_ACCURACY_THRESHOLD:
        return __RESPONSE_NO

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
