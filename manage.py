# manage.py

from flask.ext.script import Manager

from KoalaAPI import app

manager = Manager(app)


if __name__ == "__main__":
    manager.run()
