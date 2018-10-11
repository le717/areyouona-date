from os import getenv

from flask_jsglue import JSGlue
from flask_wtf.csrf import CSRFProtect

from dotenv import dotenv_values, find_dotenv

from src.core.yelp import Yelp


csrf = CSRFProtect()
jsglue = JSGlue()
yelp = Yelp()


def init_extensions(app):
    # Load the variables from the .env file into the app config
    env_vals = dotenv_values(find_dotenv())
    additional_env_vals = ("SECRET_KEY", "YELP_API_KEY")

    # Load the env values from the .env file
    for key, value in env_vals.items():
        app.config[key] = (value if value != "" else None)

    # Load the additional env values from manual setting
    for val in additional_env_vals:
        app.config[val] = getenv(val)

    # Load app exensions
    csrf.init_app(app)
    jsglue.init_app(app)
    yelp.init_app(app)
