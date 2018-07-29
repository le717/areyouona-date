import math

from src.extensions import yelp


__all__ = ["make"]


# Common values used in making an assessment
__RESPONSE_NO = "no"
__RESPONSE_MAYBE = "maybe"
__RESPONSE_YES = "yes"
__ABSURD_ACCURACY_THRESHOLD = 1000


def __get_price_rating(val: str) -> int:
    """Get the Yelp Price rating for the business.

    Yelp returns a string of dollar signs for the price tier
    but we need it as a number value.

    @param {String} val - The Yelp Price rating
    @return {Integer} The price rating expressd as a number.
    """
    return len(val)


def __get_closest_restaurant(yelp_response: dict) -> dict:
    # Find the restaurant closest to us
    restaurant = None
    closest_distance = min(r["distance"] for r in yelp_response["businesses"])

    # Now, using the distance of the closest restaurant,
    # find the business info from the Yelp data
    for r in yelp_response["businesses"]:
        if r["distance"] == closest_distance:
            restaurant = r
            break
    return restaurant


def make(user_details: dict) -> str:
    # The Geolocation API responded with data that contained
    # an absurd accuracy meter distance. Toss it out.
    # It's too late for that white horse to come around
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
        "limit": 5,
        "sort_by": "rating",
        # TODO Apparently there's an undocumented price value of "4"?!?
        "price": "1,2,3"
    }

    # Get a response from the Yelp API
    # and find the closest restaurant
    r = yelp.make_cached_request(url_params)
    restaurant = __get_closest_restaurant(r)
    return __RESPONSE_NO
