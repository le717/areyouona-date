from src.extensions import yelp
from src.core import stats


__all__ = ["make"]


# Common values used in making an assessment
__RESPONSE_NO = "no"
__RESPONSE_YES = "yes"
__RESPONSE_MAYBE = "maybe"
__ABSURD_ACCURACY_THRESHOLD = 403
__MAXIMUM_SEARCH_RADIUS = 1610


def __get_closest_restaurant(yelp_response: dict) -> dict:
    """Identify the restaurant closest to the user's location."""
    # We didn't find any restaurants so we can't assess anything
    if yelp_response["total"] == 0:
        return {}

    # Only one restaurant was found, go ahead and return it
    if yelp_response["total"] == 1:
        return yelp_response["businesses"][0]

    # Two or more restaurants were found, get the restaurant closest to us
    # It is the one we are most likely at
    closest_distance = min(r["distance"] for r in yelp_response["businesses"])

    # Now, using our distance to the closest restaurant,
    # extract the business info
    restaurant = None
    for r in yelp_response["businesses"]:
        if r["distance"] == closest_distance:
            restaurant = r
            break
    return restaurant


def __interpret_score(score: float, college_student: bool) -> str:
    # Define the assesment result ranges,
    # which are the upper-half values of the emperical rule
    # except for the college ranges,
    # which are the upper-half values further divided in half
    rating_scale = {
        "normal": {
            __RESPONSE_NO: [0, 0.99],
            __RESPONSE_YES: [2, 3],
            __RESPONSE_MAYBE: [1, 1.99]
        },
        "college": {
            __RESPONSE_NO: [0, 0.5],
            __RESPONSE_YES: [1, 2],
            __RESPONSE_MAYBE: [0.51, 0.99]
        }
    }

    # Use the appropriate rating scale depending on college student status
    scale_to_use = rating_scale["normal"]
    if college_student:
        scale_to_use = rating_scale["college"]

    # Take the absolute value of the z-score so we can use the upper half
    # of the bell curve. This makes it easier to use
    # the emperical rule as the rating scale
    score = abs(score)

    # If the z-score is somehow greater than the upper bound yes response,
    # then this is _obviously_ a date
    if score >= scale_to_use[__RESPONSE_YES][1]:
        return __RESPONSE_YES

    # Determine in what range the score falls
    # to assess if this is a date or not (or maybe)
    for k, v in scale_to_use.items():
        if score >= v[0] and score <= v[1]:
            return k


def __get_restaurant_criteria(rest: dict) -> list:
    """Get the relevant restaurant criteria."""
    # The criteria values we are interested in are as follows:
    # Index 0: Rating
    # Index 1: Review count
    # Index 2: Price
    # For restaurant price stats, Yelp returns a string of dollar signs
    # for the price tier. We need it as a number value.
    return [
        rest["rating"],
        rest["review_count"],
        len(rest["price"])
    ]


def __compute_restaurant_score(rest: dict, all_rests: list) -> float:
    # In order to calculate an assessment, we must have a sample size
    # where n >= 2. We don't have that, so we can't determine what's up.
    # We'll "determine" a z-score of 0 to indicate our inability
    if len(all_rests) < 2:
        return 0.0

    # Collect the restaurant stats for this restaurant and all
    # restaurants found in the area. This is performed by calculating a
    # z-score for the restaurant we are currently at
    rest_stats = __get_restaurant_criteria(rest)

    # Calculate the sample mean for all the restaurants
    # using the same criteria values for a mean
    all_rests_stats = []
    for r in all_rests:
        r_stats = __get_restaurant_criteria(r)
        all_rests_stats.append(stats.calculate_mean(r_stats))

    # Calculate a z-score for this restaurant
    rest_mean = stats.calculate_mean(rest_stats)
    sample_mean = stats.calculate_mean(all_rests_stats)
    sd = stats.calculate_sd(sample_mean, all_rests_stats)
    z_score = stats.calculate_z(rest_mean, sample_mean, sd)
    return z_score


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
        "radius": __MAXIMUM_SEARCH_RADIUS,
        "categories": "restaurants",
        "locale": user_details["locale"],
        "limit": 10,
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

    # Calculate the restaurant score and assess the date status
    score = __compute_restaurant_score(restaurant, r["businesses"])
    return __interpret_score(score, user_details["col"])
