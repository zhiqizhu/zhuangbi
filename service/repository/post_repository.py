from service import dbaccess
from datetime import datetime


def save_post(post):
    return dbaccess.insert("INSERT INTO t_post(title, content, created_at, author) VALUES (?,?,?,?)", post.title,
                           post.content, datetime.now(), post.author_id
                           )


def post_list(page, size):
    sql = "SELECT * FROM t_post LIMIT %s, %s" % ((page - 1) * size, size)
    return dbaccess.query_for_map(sql)
