# manage.py
from cloud import engine

from flask.ext.script import Manager

from KoalaAPI import create_app
import leancloud
import os

app = create_app()

manager = Manager(app)

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ.get('LC_APP_PORT', 3000))


leancloud.init(APP_ID, master_key=MASTER_KEY)

application = engine


if __name__ == "__main__":
    app.debug = True
    manager.run()
