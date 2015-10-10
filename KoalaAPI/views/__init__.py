from flask import Blueprint
from leancloud import Object

main_view = Blueprint('main', __name__)

__all__ = ['tuchuang', 'auth']

GitHubUser = Object.extend('GitHubUser')
File = Object.extend('Files')

from . import *
