# coding=utf-8
from . import main_view, GitHubUser, File, leanobject_to_dict
from datetime import datetime
from flask import render_template, request, session, redirect, url_for, current_app, flash
from leancloud import Query
from qiniu import put_data, Auth

__author__ = 'bohan'


@main_view.route('/tuchuang', methods=['GET', 'POST'])
def tuchuang_index():
    github_user = _get_user()

    if not github_user:
        flash(u'请正确完成牛逼参数设置后上传图片！', category='warning')
        return redirect(url_for('.info'))

    if request.method == 'POST':
        access_key = str(github_user.get('access_key'))
        secret_key = str(github_user.get('secret_key'))
        bucket_name = str(github_user.get('bucket_name'))
        domain_name = str(github_user.get('domain_name'))
        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)

        upload_files = request.files.getlist('file')
        for upload_file in upload_files:
            key = '%s_%s' % (datetime.now().isoformat(), upload_file.filename)
            ret, info = put_data(up_token=token, key=key, data=upload_file)
            url = '%s/%s' % (domain_name, key)
            f = File()
            f.set('url', url)
            f.set('user', github_user)
            f.save()
        flash(u'成功上传%s张照片！' % len(upload_files), category='success')
        return redirect(url_for('.tuchuang_index'))

    image_id = request.args.get('image_id')
    image = Query(File).get(image_id) if image_id else None

    return render_template('tuchuang.html', image=image)


@main_view.route('/tuchuang/list')
def tuchuang_list():
    github_user = _get_user()
    if not github_user:
        return redirect(url_for('.info'))

    return render_template('tuchuang_list.html')


@main_view.route('/tuchuang/waterfall')
def tuchuang_waterfall_html():
    github_user = _get_user()

    page = int(request.args.get('page', 1))
    page_size = 20
    images = Query(File).equal_to('user', github_user).descending('createdAt').skip((page - 1) * page_size).limit(page_size).find()
    str = ''
    for image in images:
        str += u'''
<div class="item" >
    <img src="{url}?imageView2/2/w/192" width="192">
</div>
'''.format(url=image.get('url'))

    return str


def _get_user():
    user = session.get('user')
    if not user:
        return
    github_user = Query(GitHubUser).get(user.get('id'))

    if not github_user.get('qiniu_ok'):
        return
    return github_user
