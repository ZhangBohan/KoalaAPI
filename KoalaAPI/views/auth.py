from . import main_view, GitHubUser
from flask import render_template, request, abort, current_app, redirect, url_for, session
from leancloud import LeanCloudError, Query
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

    try:
        query = Query(GitHubUser)
        user = query.equal_to('email', github_user.get('email')).first()
    except LeanCloudError as e:
        user = _register(github_user)

    session['user'] = {
        'email': user.get('email'),
        'avatar_url': user.get('avatar_url'),
        'username': user.get('username'),
        'access_key': user.get('access_key'),
        'secret_key': user.get('secret_key'),
        'bucket_name': user.get('bucket_name'),
    }
    return redirect(url_for('.tuchuang_index', result=result.text))


def _register(github_user):
    user = GitHubUser()
    user.set("username", github_user.get('login'))
    user.set("email", github_user.get('email'))
    user.set("avatar_url", github_user.get('avatar_url'))
    user.save()
    return user
