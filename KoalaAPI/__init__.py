from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    app.config['client_id'] = 'b36fd04ccb202122a5c7'
    app.config['client_secret'] = '652be8dcb4bebbb5efec0828a2ef302816f0e006'

    from .api_v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix="/v1")

    from .views import main_view as main_view_blueprint
    app.register_blueprint(main_view_blueprint, url_prefix="")
    return app
