# coding=utf-8
from . import main_view, GitHubUser, leanobject_to_dict
from flask import render_template, request, abort, current_app, redirect, url_for, session, flash
from leancloud import LeanCloudError, Query
from qiniu import Auth, BucketManager
import requests

__author__ = 'bohan'


@main_view.route('/auth/login')
def login():
    return render_template('login.html')


@main_view.route('/auth/info', methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        user = Query(GitHubUser).get(session.get('user').get('id'))

        access_key = str(request.form.get('ak'))
        secret_key = str(request.form.get('sk'))
        bucket_name = str(request.form.get('bn'))
        user.set('access_key', access_key)
        user.set('secret_key', secret_key)
        user.set('bucket_name', bucket_name)
        user.save()
        _upload_qiniu_token_or_redirect(user)
        session['user'] = leanobject_to_dict(user)
        flash(u'您已正确填写七牛信息，可以开始使用该图床了', category='success')
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

        _upload_qiniu_token_or_redirect(user)
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
    if user.has_qiniu():
        q = Auth(str(user.get('access_key')), str(user.get('secret_key')))
        bucket = BucketManager(q)
        result = bucket.list(str(user.get('bucket_name')), limit=1)  # 验证该bucket是否可用
        # 如果bucket不存在，则会抛出631错误，在此进行错误处理
        if result[2].status_code == 631:
            flash(u'不存在该bucket，请确认是否填写正确！', category='warning')
            return redirect(url_for('.info'))

        token = q.upload_token(user.get('bucket_name'))
        session['qiniu_token'] = token
    else:
        flash(u'资料不全，请填写完全！', category='warning')
        return redirect(url_for('.info'))
