class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Post:
    def __init__(self, title, content, created_at=None, author_id=None, updated_at=None, img_url = None):
        self.author_id = author_id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.img_url = img_url


class Comment:
    def __init__(self, body, author, post_id,created_at):
        self.body = body
        self.author = author
        self.post_id = post_id
        self.created_at = created_at