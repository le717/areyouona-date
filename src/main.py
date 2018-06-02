from flask import Flask
from flask_jsglue import JSGlue
from src.blueprint import blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint.bp)

    jsglue = JSGlue()
    jsglue.init_app(app)

    return app