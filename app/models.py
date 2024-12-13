from datetime import datetime

from .config import get_timezone


class User:

    def __init__(self, user_id: int, username: str, password: str,
                 created_at: datetime, bio: str | None = None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.created_at = created_at + get_timezone()
        self.bio = bio

    def __repr__(self):
        return f'<Remlink User: {self.username}>'


class Privacy:

    def __init__(self, privacy: str):
        self.privacy = privacy

    def is_valid(self) -> bool:
        return self.privacy in {'public', 'friends', 'private'}

    def __repr__(self):
        return {
            'public': '公开',
            'friends': '好友圈',
            'private': '私密'
        }[self.privacy]


class Post:

    def __init__(self, post_id: int, user_id: int, username: str,
                 content: str, created_at: datetime, privacy: str,
                 bio: str | None = None, like_count: int = 0,
                 follower_count: int = 0, followee_count: int = 0,
                 liked: int = 0, owned: int = 0,
                 following: int = 0, followed: int = 0):
        self.post_id = post_id
        self.content = content
        self.created_at = created_at + get_timezone()
        self.privacy = Privacy(privacy)
        self.like_count = like_count
        self.liked = bool(liked)
        self.owned = bool(owned)
        self.author = Profile(
            user_id, username, bio, follower_count, followee_count,
            followed, following)

    def __repr__(self):
        return f'<Remlink Post: {self.post_id}>'


class Profile:

    def __init__(self, user_id: int, username: str, bio: str | None = None,
                 follower_count: int = 0, followee_count: int = 0,
                 following: int = 0, followed: int = 0):
        self.user_id = user_id
        self.username = username
        self.bio = bio
        self.follower_count = follower_count
        self.followee_count = followee_count
        self.following = bool(following)
        self.followed = bool(followed)

    def __repr__(self):
        return f'<Remlink Profile: {self.username}>'
