from . import main_view
import json
from os import abort
from flask import render_template, request, url_for, current_app
from qiniu import Auth, put_data
import uuid
import requests

__author__ = 'bohan'


@main_view.route('/tuchuang', methods=['GET', 'POST'])
def tuchuang_index():
    url = access_key = secret_key = bucket_name = None

    if request.method == 'POST':
        access_key = str(request.form.get('ak'))
        secret_key = str(request.form.get('sk'))
        bucket_name = str(request.form.get('bn'))
        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)

        key = str(uuid.uuid1())
        ret, info = put_data(up_token=token, key=key, data=request.files.get('file'))
        url = 'http://%s.qiniudn.com/%s' % (bucket_name, key)
    return render_template('tuchuang.html', url=url, access_key=access_key, secret_key=secret_key,
                           bucket_name=bucket_name)


@main_view.route('/tuchuang/callback')
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
        # 'redirect_uri': url_for('.tuchuang_index', _external=True)
    }
    result = requests.get(url, params, headers={'Accept': 'application/json'})
    data = json.loads(result)
    params = {"access_token": data.get('access_token')}
    result = requests.get('https://api.github.com/user', params)
    current_app.logger.debug('result: %s' % result)
    return url_for('.tuchuang_index', result=result)
