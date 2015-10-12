# coding=utf-8
from . import main_view, GitHubUser, leanobject_to_dict
from flask import render_template, request, abort, current_app, redirect, url_for, session, flash, get_flashed_messages
from leancloud import LeanCloudError, Query
from qiniu import Auth, put_data
import requests

__author__ = 'bohan'


@main_view.route('/auth/login')
def login():
    return render_template('login.html')


@main_view.route('/auth/info', methods=['GET', 'POST'])
def info():
    if not session.get('user'):
        redirect(url_for('.login'))

    if request.method == 'POST':
        user = Query(GitHubUser).get(session.get('user').get('id'))

        user.set('access_key', request.form.get('ak'))
        user.set('secret_key', request.form.get('sk'))
        user.set('bucket_name', request.form.get('bn'))
        user.set('domain_name', request.form.get('dn'))
        _upload_qiniu_token_or_redirect(user)
        session['user'] = leanobject_to_dict(user)
        flash(u'您已正确填写七牛信息，可以开始使用该图床了', category='success')

        user.save()
        return redirect(url_for('.info'))
    return render_template('info.html')


@main_view.route('/auth/logout')
def logout():
    session.pop('user')
    flash(u'退出成功！', category='success')
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

        session['user'] = leanobject_to_dict(user)
        flash(u'欢迎回来！', category='success')
        return redirect(url_for('.tuchuang_index', result=result.text))
    except LeanCloudError as e:
        _register(github_user)
        flash(u'恭喜你注册成功，请填写七牛资料', category='success')
        return redirect(url_for('.info'))


def _register(github_user):
    user = GitHubUser()
    user.set("username", github_user.get('login'))
    user.set("email", github_user.get('email'))
    user.set("avatar_url", github_user.get('avatar_url'))
    user.save()
    return user


def _upload_qiniu_token_or_redirect(user):
    access_key = str(user.get('access_key'))
    secret_key = str(user.get('secret_key'))
    bucket_name = str(user.get('bucket_name'))
    domain_name = str(user.get('domain_name'))
    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name)
    ret, info = put_data(token, key='foo', data='bar')
    # 如果bucket不存在，在此进行错误处理
    if info.status_code != 200:
        flash(u'七牛数据错误，错误：%s！' % info.error, category='error')
        return redirect(url_for('.info'))
    url = '{domain_name}/{key}'.format(domain_name=domain_name, key='foo')
    if requests.get(url).text != 'bar':
        flash(u'域名错误！', category='error')
    user.set('qiniu_ok', True)
