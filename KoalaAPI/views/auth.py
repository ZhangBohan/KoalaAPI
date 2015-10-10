from . import main_view
from flask import render_template, request, abort, current_app, redirect, url_for, session
from leancloud import User, LeanCloudError
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

    github_user = result.json()
    current_app.logger.debug('result: %s' % github_user)
    user = None
    try:
        user = User().login(github_user.get('email'), github_user.get('id'))
    except LeanCloudError as e:
        if 211 == e.code:   # not register yet
            user = _register(github_user)

    session['user'] = user
    return redirect(url_for('.tuchuang_index', result=result.text))


def _register(github_user):
    user = User()
    user.set("username", github_user.get('email'))
    user.set("password", github_user.get('id'))
    user.set("email", github_user.get('email'))
    # user.set("avatar_url", github_user.get('avatar_url'))
    user.sign_up()
    return user
