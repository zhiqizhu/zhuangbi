from service import dbaccess
from datetime import datetime


def save_post(post):
    return dbaccess.insert("INSERT INTO t_post(title, content, created_at, author, img_url) VALUES (?,?,?,?,?)", post.title,
                           post.content, datetime.now(), post.author_id, post.img_url
                           )


def post_list(page, size):
    sql = "SELECT * FROM t_post LIMIT %s, %s" % ((page - 1) * size, size)
    return dbaccess.query_for_map(sql)


def post_count():
    sql = "SELECT COUNT(1) as total FROM t_post"
    return dbaccess.query_for_map(sql)


def post_detail(post_id):
    sql = "SELECT * FROM t_post WHERE id = ?"
    post = dbaccess.query_for_map(sql, post_id)
    if not post: return post
    sql = "SELECT * FROM t_comment WHERE post_id = ?"
    comments = dbaccess.query_for_map(sql, post_id)
    p = post[0]
    p['comments'] = comments
    return p
