from . import main_view
from flask import render_template, request
from qiniu import Auth, put_data
import uuid

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
