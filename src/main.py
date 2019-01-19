from flask import Flask

from dotenv import dotenv_values, find_dotenv

from src.blueprint import blueprint
from src.extensions import init_extensions


def create_app():
    app = Flask(__name__)

    # Load the variables from the .env file into the app config
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        app.config[key] = (value if value != "" else None)

    # Load any extensions and register the blueprint
    init_extensions(app)
    app.register_blueprint(blueprint.bp)
    return app
