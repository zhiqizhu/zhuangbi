import sqlite3, os

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, current_app
import datetime
import itertools

connection_cache = None


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    # if not hasattr(g, 'sqlite_db'):
    #     g.sqlite_db = connect_db()
    # with g.sqlite_db as conn:
    #     conn.row_factory = sqlite3.Row
    # return g.sqlite_db
    global connection_cache
    if connection_cache is None:
        connection_cache = connect_db()
    return connection_cache


def connect_db():
    with current_app.app_context():
        return sqlite3.connect(current_app.config['DATABASE'])
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # return sqlite3.connect(os.path.join(dir_path, 'zhuangbi.db'))


def init_db():
    db = get_db()
    with current_app.open_resource('db/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def __dict_gen(curs):
    field_names = [d[0].lower() for d in curs.description]
    result = []
    rows = curs.fetchmany()
    while rows:
        for row in rows:
            result.append(dict(itertools.izip(field_names, row)))
        rows = curs.fetchmany()
    return result


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def query_for_map(query, *args):
    cur = get_db().execute(query, args)
    return __dict_gen(cur)


def insert(sql, *args):
    cur = get_db().cursor()
    cur.execute(sql, args)
    get_db().commit()
    return cur.lastrowid
