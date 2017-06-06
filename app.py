# coding=utf-8
import os
import sys

from flask import Flask, request, g, render_template, flash, jsonify, session

from service.model import models
from service.repository import user_repository
from service.repository import post_repository

import flask_login
from service.util import cors_util

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

reload(sys)
sys.setdefaultencoding("utf-8")
print "encoding set"


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


@login_manager.user_loader
def load_user(user_id):
    users = user_repository.find_by_dict({"id": user_id})
    if users:
        return users[0]
    return None


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
