from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)

__all__ = ['qr_views', 'pinyin_views']

from . import *
