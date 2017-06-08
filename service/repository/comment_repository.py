import dbaccess


def save_comment(comment):
    return dbaccess.insert("INSERT INTO t_comment(body, post_id, created_at, author) VALUES (?,?,?,?)",
                           comment.body, comment.post_id, comment.created_at, comment.author
                           )
