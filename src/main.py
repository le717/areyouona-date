from dotenv import dotenv_values, find_dotenv

from flask import Flask
from flask_jsglue import JSGlue
from flask_wtf.csrf import CSRFProtect

from src.blueprint import blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint.bp)

    # Load the environment variables from .env file
    env_vals = dotenv_values(find_dotenv())
    for key in env_vals:
        value = env_vals[key]
        app.config[key] = (value if value != "" else None)

    # Load app exensions
    jsglue = JSGlue()
    jsglue.init_app(app)
    csrf = CSRFProtect()
    csrf.init_app(app)

    return app
