from . import main_view, GitHubUser, File
from datetime import datetime
from flask import render_template, request, session, redirect, url_for
from leancloud import Query
from qiniu import Auth, put_data
import uuid

__author__ = 'bohan'


@main_view.route('/tuchuang', methods=['GET', 'POST'])
def tuchuang_index():
    user = session.get('user')
    if not user:
        return redirect(url_for('.login'))

    url = access_key = secret_key = bucket_name = None

    if request.method == 'POST':
        access_key = str(request.form.get('ak'))
        secret_key = str(request.form.get('sk'))
        bucket_name = str(request.form.get('bn'))
        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)

        upload_file = request.files.get('file')
        key = '%s_%s' % (datetime.now().isoformat(), upload_file.filename)
        ret, info = put_data(up_token=token, key=key, data=upload_file)
        url = 'http://%s.qiniudn.com/%s' % (bucket_name, key)
        f = File()
        f.set('url', url)
        f.save()

        query = Query(GitHubUser)
        user = query.equal_to('email', user.get('email')).first()
        user.set('access_key', access_key)
        user.set('secret_key', secret_key)
        user.set('bucket_name', bucket_name)
        user.save()
    return render_template('tuchuang.html', url=url)
