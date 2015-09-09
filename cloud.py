# coding: utf-8

from KoalaAPI import create_app
from leancloud import Engine

app = create_app()


engine = Engine(app)


@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'
