from dotenv import dotenv_values, find_dotenv

from flask_jsglue import JSGlue
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()
jsglue = JSGlue()


def init_extensions(app):
    # Load the variables from the .env file into the app config
    env_vals = dotenv_values(find_dotenv())
    for key, value in env_vals.items():
        app.config[key] = (value if value != "" else None)

    # Load app exensions
    csrf.init_app(app)
    jsglue.init_app(app)
