from flask_analytics import Analytics
from flask_jsglue import JSGlue
from flask_wtf.csrf import CSRFProtect

from src.core.yelp import Yelp

analytics = analytics()
csrf = CSRFProtect()
jsglue = JSGlue()
yelp = Yelp()


def init_extensions(app):
    # Load app exensions
    analytics.init_app(app, None)
    csrf.init_app(app)
    jsglue.init_app(app)
    yelp.init_app(app)
