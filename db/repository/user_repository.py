import dbaccess
from model.models import User


def save_user(user):
    return dbaccess.insert("insert into t_user(user_name, mail, pass_word) values (?,?,?)", user.username, user.email,
                           user.password)


def find_by_email(mail):
    result = dbaccess.query_for_map("select * from t_user where mail=?", mail)
    return result


def find_by_dict(dict):
    if not dict:
        return None
    sql = "select * from t_user where "
    values = []
    is_first_round = True
    for key, value in dict.iteritems():
        if (is_first_round):
            sql += "%s=? " % key
        else:
            sql += "and %s=? " % key
        values.append(value)
        is_first_round = False
    return dbaccess.query_for_map(sql, *tuple(values))
