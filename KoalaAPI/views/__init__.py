from flask import Blueprint

main_view = Blueprint('main', __name__)

__all__ = ['tuchuang', 'auth']

from . import *
