# coding=utf-8
import os
import sys

from flask import Flask, request, g, render_template

from model import models
from repository import user_repository

app = Flask(__name__)

reload(sys)
sys.setdefaultencoding("utf-8")
print "encoding set"


@app.route('/')
def hello_world():
    return 'Hello World!'


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


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    # Load default config
    app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'db/zhuangbi.db'),
        SECRET_KEY='development key',
        USERNAME='admin',
        PASSWORD='default'
    ))

    app.run(host='0.0.0.0', debug=True)


# override config from an environment variable
# app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
