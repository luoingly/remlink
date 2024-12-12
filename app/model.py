from datetime import datetime


class User:

    def __init__(self, user_id: int, username: str, password: str,
                 created_at: datetime, bio: str | None = None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.created_at = created_at
        self.bio = bio

    def __repr__(self):
        return f'<User {self.username}>'
