from flask import Blueprint
from leancloud import Object

main_view = Blueprint('main', __name__)

__all__ = ['tuchuang', 'auth']


class GitHubUser(Object):
    pass

File = Object.extend('Files')


def leanobject_to_dict(lo):
    data = lo.attributes
    data['id'] = lo.id
    data['created_at'] = lo.created_at
    data['updated_at'] = lo.updated_at
    return data

from . import *
