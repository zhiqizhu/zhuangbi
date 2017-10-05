# coding=utf-8
import os
import sys

from datetime import datetime
import jinja2
from flask import Flask, request, g, render_template, flash, jsonify, session, json

from service.model import models
from service.repository import user_repository
from service.repository import post_repository
from service.repository import comment_repository
from service.util import cors_util

app = Flask(__name__, template_folder='static/html', static_url_path='')
reload(sys)
sys.setdefaultencoding("utf-8")
print "encoding se"


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/auto_complete')
def auto_complete():
    searchword = request.args.get('searchword', '')
    return jsonify({'hint': searchword + random_str(5)})


@app.route('/validate')
def validate():
    phoneNo = request.args.get('phoneNo', '')
    if (phoneNo == '15881087265'):
        return jsonify({'code': 'OK'})
    return jsonify({'code': 'FAIL'})


from random import Random


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def initdb_command():
    """Initializes the database."""
    # dbaccess.init_db()
    print 'Initialized the database.'


@app.route('/api/login', methods=['POST'])
@cors_util.crossdomain(origin='*')
def login():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    # mail = request.form.get('email', None)
    # user = models.User(username=username, password=password, email=mail)
    # if flask_login.login_user(user):
    user = user_repository.find_by_dict({"user_name": username, "pass_word": password})
    if user:
        session['login_user'] = user
        flash('Logged in successfully.')
        return jsonify({'code': 'OK'})
    else:
        return jsonify({'code': 'FAIL'})


@app.route('/api/register', methods=['POST'])
@cors_util.crossdomain(origin='*')
def register_api():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    mail = request.form.get('email', None)
    if not username:
        return jsonify({'code': 'FAIL', 'message': '用户名为空'})
    if not password:
        return jsonify({'code': 'FAIL', 'message': '密码为空'})
    if not mail:
        return jsonify({'code': 'FAIL', 'message': '邮箱为空'})
    existed = user_repository.find_by_email(mail)
    if existed:
        return jsonify({'code': 'FAIL', 'message': '用户邮箱已经被注册'})
    else:
        user = models.User(username=username, password=password, email=mail)
        user_repository.save_user(user)
        return jsonify({'code': 'SUCCESS'})


@app.route('/api/post', methods=['POST'])
@cors_util.crossdomain(origin='*')
def save_post():
    title = request.form.get('title', None)
    content = request.form.get('content', None)
    user = None
    if 'login_user' in session:
        user = session['login_user']

    if not title:
        return jsonify({'code': 'FAIL', 'message': '标题为空'})
    if not content:
        return jsonify({'code': 'FAIL', 'message': '内容为空'})
    if user:
        post = models.Post(title=title, content=content, author_id=user.username)
    else:
        post = models.Post(title=title, content=content)
    post_repository.save_post(post)
    return jsonify({'code': 'SUCCESS'})


@app.route('/api/post', methods=['GET'])
@cors_util.crossdomain(origin='*')
def list_post():
    page = request.args.get('page')
    size = request.args.get('size')
    page = 1 if not page else int(page)
    size = 10 if not size else int(size)
    result = post_repository.post_list(page=page, size=size)
    total = post_repository.post_count()
    print total[0]
    return jsonify({'total': total[0]['total'],'data':result})


@app.route('/api/comment', methods=['POST'])
@cors_util.crossdomain(origin='*')
def post_comment():
    post_id = request.form.get('post_id', None)
    body = request.form.get('body', None)
    if not post_id or not body:
        return jsonify({'code': 'FAIL', 'message': '参数不对'})
    user = None
    if 'login_user' in session:
        user = session['login_user']
    comment = models.Comment(body, user, int(post_id), datetime.now())
    comment_repository.save_comment(comment)
    return jsonify({'code': 'SUCCESS'})


@app.route('/api/post/<int:post_id>', methods=['GET'])
@cors_util.crossdomain(origin='*')
def post_detail(post_id):
    return jsonify(post_repository.post_detail(post_id))\



@app.route('/api/banners', methods=['GET'])
@cors_util.crossdomain(origin='*')
def banner_list():
    json_url = os.path.join(app.root_path, "static/js", "img.json")
    with open(json_url) as banner_json:
        data = json.load(banner_json)
        return jsonify(data)

if __name__ == '__main__':
    # Load default config
    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'service/zhuangbi.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default'
    ))

    # override config from an environment variable
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    # Heroku dynamically assigns app a port
    port = int(os.environ.get('PORT', 5000))

    app.run(host='127.0.0.1', debug=True, port=port)


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
