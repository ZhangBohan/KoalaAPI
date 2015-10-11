from . import main_view, GitHubUser, File, leanobject_to_dict
from datetime import datetime
from KoalaAPI.views.auth import _upload_qiniu_token_or_redirect
from flask import render_template, request, session, redirect, url_for, current_app
from leancloud import Query
from qiniu import Auth, put_data

__author__ = 'bohan'


@main_view.route('/tuchuang', methods=['GET', 'POST'])
def tuchuang_index():
    user = session.get('user')
    if not user:
        if current_app.debug:
            github_user = Query(GitHubUser).first()
            user = leanobject_to_dict(github_user)
            session['user'] = user
            _upload_qiniu_token_or_redirect(github_user)
        else:
            return redirect(url_for('.login'))
    github_user = Query(GitHubUser).get(user.get('id'))

    if not session.get('qiniu_token'):
        return redirect(url_for('.info'))

    if request.method == 'POST':

        upload_file = request.files.get('file')
        if upload_file.content_length == 0:
            redirect(url_for('.tuchuang_index'))
        key = '%s_%s' % (datetime.now().isoformat(), upload_file.filename)
        ret, info = put_data(up_token=session.get('qiniu_token'), key=key, data=upload_file)
        url = 'http://%s.qiniudn.com/%s' % (github_user.get('bucket_name'), key)
        f = File()
        f.set('url', url)
        f.set('user', github_user)
        f.save()

        return redirect(url_for('.tuchuang_index', image_id=f.id))

    image_id = request.args.get('image_id')
    image = Query(File).get(image_id) if image_id else None

    return render_template('tuchuang.html', image=image)


@main_view.route('/tuchuang/list')
def tuchuang_list():
    return render_template('tuchuang_list.html')

