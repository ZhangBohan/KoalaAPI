from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    app.config['client_id'] = os.environ['client_id']
    app.config['client_secret'] = os.environ['client_secret']

    from .api_v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix="/v1")

    from .views import main_view as main_view_blueprint
    app.register_blueprint(main_view_blueprint, url_prefix="")
    return app
