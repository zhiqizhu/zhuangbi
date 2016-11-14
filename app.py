# coding=utf-8
import os
import sys

from flask import Flask, request, g, render_template, flash, jsonify, session

from service.model import models
from service.repository import user_repository

import flask_login

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


@app.route('/register', methods=['POST'])
def do_register():
    error = None
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    mail = request.form.get('email', None)
    if (not username) or (not password) or (not mail):
        error = "请正确输入表单!"
        return render_template('register.html', error=error)
    else:
        existed = user_repository.find_by_email(mail)
        if existed:
            error = "用户邮箱已经被注册"
            return render_template('register.html', error=error)
        else:
            user = models.User(username=username, password=password, email=mail)
            user_repository.save_user(user)
            return 'register success!'


@app.route('/register', methods=['GET'])
def to_register():
    return render_template('register.html')


@app.route('/login', methods=['POST'])
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


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/api', methods=['GET'])
def test_api():
    login_user = session.get('login_user', None)
    if not login_user:
        return jsonify({'code': 403})
    return "success"


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

    app.run(host='0.0.0.0', debug=True, port=port)


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
