import time
from flask import Blueprint, render_template

bp = Blueprint("date", __name__, url_prefix="")


@bp.app_context_processor
def cache_buster():
    return {"cache_buster": time.time()}


@bp.route("/")
def index():
    r = render_template("no.html")
    r = render_template("yes.html")
    return render_template("index.html", **{"result": r})
