import time
from flask import Blueprint, request
from flask import render_template, url_for

import src.core.assessment as assessment


bp = Blueprint("date", __name__, url_prefix="")


@bp.app_context_processor
def cache_buster() -> dict:
    return {"cache_buster": time.time()}


@bp.route("/form", methods=["POST"])
def form() -> str:
    # Get the user's preferred locale, for use when interacting with Yelp
    request.json["locale"] = request.accept_languages.best.replace("-", "_")

    # Make an assessment regarding the user's date status
    result = assessment.make(request.json)
    responses = {
        "no": url_for("date.no"),
        "yes": url_for("date.yes"),
        "maybe": url_for("date.maybe"),
    }
    return responses[result]


@bp.route("/")
def index() -> str:
    return render_template("permission.html")


@bp.route("/privacy")
def privacy() -> str:
    return render_template("privacy.html", page_title="Privacy")


@bp.route("/no")
def no() -> str:
    return render_template("no.html", page_title="No.")


@bp.route("/maybe")
def maybe() -> str:
    return render_template("maybe.html", page_title="Maybe...?")


@bp.route("/yes")
def yes() -> str:
    return render_template("yes.html", page_title="Yes!")


@bp.app_errorhandler(404)
def page_not_found(e) -> str:
    return render_template("error.html", page_title="Status: Unavailable"), 404


@bp.app_errorhandler(500)
def internal_server_error(e) -> str:
    return render_template(
        "error.html",
        page_title="Status: Incapable of love"
    ), 500
