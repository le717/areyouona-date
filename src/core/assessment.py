import math

from src.extensions import yelp


__all__ = ["make"]


# Common values used in making an assessment
__RESPONSE_NO = "no"
__RESPONSE_YES = "yes"
__RESPONSE_MAYBE = "maybe"
__ABSURD_ACCURACY_THRESHOLD = 1000


def __convert_price_rating(val: str) -> int:
    """Get the Yelp Price rating for the business.

    Yelp returns a string of dollar signs for the price tier
    but we need it as a number value.

    @param {String} val - The Yelp Price rating
    @return {Integer} The price rating expressd as a number.
    """
    return len(val)


def __get_closest_restaurant(yelp_response: dict) -> dict:
    # We didn't find any restaurants so we can't assess anything
    if yelp_response["total"] == 0:
        return {}

    # Only one restaurant was found, go ahead and return it
    if yelp_response["total"] == 1:
        return yelp_response["businesses"][0]

    # Two or more restaurants were found, get the restaurant closest to us
    closest_distance = min(r["distance"] for r in yelp_response["businesses"])

    # Now, using our distance to the closest restaurant,
    # extract the business info
    restaurant = None
    for r in yelp_response["businesses"]:
        if r["distance"] == closest_distance:
            restaurant = r
            break
    return restaurant


def __compute_restaurant_score(restaurant: dict) -> float:
    # Define the weights for each metric and restaurant stats
    # The weight criteria, in order of index, are as follows:
    # Index 0: Rating
    # Index 1: Review count
    # Index 2: Price
    # TODO Calculate actual weights
    weights = [1, 1, 1]
    stats = [
        restaurant["rating"],
        restaurant["review_count"],
        __convert_price_rating(restaurant["price"])
    ]

    # Compute the weighted average
    # Taken from https://stackoverflow.com/a/29330897
    # TODO Possibly round to 2 or 3 decimal places
    avg = sum(x * y for x, y in zip(stats, weights)) / sum(weights)
    return avg


def make(user_details: dict) -> str:
    # The Geolocation API responded with data that contained
    # an absurd accuracy meter distance. Toss it out.
    # It's too late for that white horse to come around
    # https://developer.mozilla.org/en-US/docs/Web/API/Coordinates
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
        "price": "1,2,3,4"
    }

    # Get a response from the Yelp API
    # and find the closest restaurant
    r = yelp.make_cached_request(url_params)
    restaurant = __get_closest_restaurant(r)

    # ...Except Yelp couldn't find a restaurant we might be at
    if not restaurant:
        return __RESPONSE_NO
    return __RESPONSE_NO
