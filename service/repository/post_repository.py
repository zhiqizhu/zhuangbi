from service import dbaccess
from datetime import datetime


def save_post(post):
    return dbaccess.insert("insert into t_post(title, content, created_at, author) values (?,?,?,?)", post.title,
                           post.content, datetime.now(), post.author_id
                           )
