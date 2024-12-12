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


class Post:

    def __init__(self, post_id: int, user_id: int, content: str,
                 created_at: datetime, privacy: str,
                 like_count: int, comment_count: int, liked: int):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at
        self.privacy = privacy
        self.like_count = like_count
        self.comment_count = comment_count
        self.liked = bool(liked)

    def __repr__(self):
        return f'<Post {self.post_id}>'
