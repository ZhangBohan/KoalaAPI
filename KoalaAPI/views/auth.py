from . import main_view
from flask import render_template, request, abort, current_app, redirect, url_for, session
import requests

__author__ = 'bohan'


@main_view.route('/auth/login')
def login():
    return render_template('login.html')


@main_view.route('/auth/logout')
def logout():
    session.pop('user')
    return redirect('.login')


@main_view.route('/auth/callback')
def tuchuang_callback():
    code = request.args.get('code')
    if not code:
        abort(404)

    url = 'https://github.com/login/oauth/access_token'
    config = current_app.config
    params = {
        'client_id': config.get('client_id'),
        'client_secret': config.get('client_secret'),
        'code': code,
    }
    result = requests.get(url, params, headers={'Accept': 'application/json'})
    data = result.json()
    params = {"access_token": data.get('access_token')}
    result = requests.get('https://api.github.com/user', params)
    current_app.logger.debug('result: %s' % result.text)
    session['user'] = result.json()
    return redirect(url_for('.tuchuang_index', result=result.text))
