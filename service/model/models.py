class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Post:
    def __init__(self, title, content, created_at=None, author_id=None, updated_at=None):
        self.author_id = author_id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
