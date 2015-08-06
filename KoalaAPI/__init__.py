from flask import Flask


def create_app():
    app = Flask(__name__)

    from .api_v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix="/v1")

    return app
