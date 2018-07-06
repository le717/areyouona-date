import time
from flask import Blueprint, render_template

bp = Blueprint("date", __name__, url_prefix="")


@bp.app_context_processor
def cache_buster():
    return {"cache_buster": time.time()}


@bp.route("/")
def index():
    return render_template("permission.html")


@bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@bp.route("/no")
def no():
    r = render_template("no.html")
    return render_template("index.html", **{"result": r})


@bp.route("/maybe")
def maybe():
    r = render_template("maybe.html")
    return render_template("index.html", **{"result": r})


@bp.route("/yes")
def yes():
    r = render_template("yes.html")
    return render_template("index.html", **{"result": r})
