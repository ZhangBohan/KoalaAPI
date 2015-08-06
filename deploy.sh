#!/usr/bin/env bash

source env/bin/activate
git pull
pip install -r requirements.txt -q
gunicorn -w 4 wsgi:app