import re

from pymysql.cursors import DictCursor

from .utils import hash_password, check_password
from .db import get_connection, DatabaseError
from .models import User, Post, Privacy, Profile

USERNAME_REGEX = r'^[a-zA-Z0-9_]{4,20}$'
PASSWORD_REGEX = \
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$'

PAGE_SIZE = 10


class UserService:

    @staticmethod
    def _get_user_by_username(username: str) -> User | None:
        assert re.match(USERNAME_REGEX, username)

        connection = get_connection()
        query = "SELECT * FROM users WHERE username = %s"
        params = (username,)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
                user = cursor.fetchone()
            return User(**user) if user else None
        finally:
            connection.close()

    @staticmethod
    def _get_user_by_id(user_id: int) -> User:
        connection = get_connection()
        query = "SELECT * FROM users WHERE user_id = %s"
        params = (user_id,)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
                user = cursor.fetchone()
            if not user:
                raise ValueError("用户不存在。")
            return User(**user)
        except Exception as e:
            raise DatabaseError("获取用户信息失败") from e
        finally:
            connection.close()

    @staticmethod
    def register(username: str, password: str) -> User:
        if not re.match(USERNAME_REGEX, username):
            raise ValueError("用户名必须由 4-20 位字母、数字或下划线组成。")
        if not re.match(PASSWORD_REGEX, password):
            raise ValueError("密码必须包含大小写字母、数字和特殊字符，长度为 8-20 位。")
        if UserService._get_user_by_username(username) is not None:
            raise ValueError("用户名已存在，换一个试试吧。")

        connection = get_connection()
        query = \
            "INSERT INTO users (username, password) " \
            "VALUES (%s, %s) " \
            "RETURNING *"
        params = (username, hash_password(password))

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
                user = cursor.fetchone()
            connection.commit()
            return User(**user)
        except Exception as e:
            connection.rollback()
            raise DatabaseError("注册失败") from e
        finally:
            connection.close()

    @staticmethod
    def login(username: str, password: str) -> User:
        MISMATCH_ERROR = "用户名或密码错误。"

        if not re.match(USERNAME_REGEX, username):
            raise ValueError(MISMATCH_ERROR)
        if not re.match(PASSWORD_REGEX, password):
            raise ValueError(MISMATCH_ERROR)

        user = UserService._get_user_by_username(username)
        if not user or not check_password(password, user.password):
            raise ValueError(MISMATCH_ERROR)

        return user

    @staticmethod
    def get_profile(user_id: int) -> Profile:
        connection = get_connection()
        query = "SELECT * FROM users_view WHERE user_id = %s"
        params = (user_id,)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
                profile = cursor.fetchone()
            if not profile:
                raise ValueError("用户不存在。")
            return Profile(**profile)
        except Exception as e:
            raise DatabaseError("获取用户信息失败") from e
        finally:
            connection.close()

    @staticmethod
    def update_profile(user_id: int, username: str, bio: str) -> None:
        if not re.match(USERNAME_REGEX, username):
            raise ValueError("用户名必须由 4-20 位字母、数字或下划线组成。")

        if len(bio) > 100:
            raise ValueError("个人简介长度不能超过 100 字符。")

        Profile = UserService.get_profile(user_id)
        if username != Profile.username and \
                UserService._get_user_by_username(username):
            raise ValueError("用户名已存在，换一个试试吧。")

        connection = get_connection()
        query = "UPDATE users SET username = %s, bio = %s WHERE user_id = %s"
        params = (username, bio.replace(
            '\r\n', '\n').replace('\n', ' '), user_id)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise DatabaseError("更新用户信息失败") from e
        finally:
            connection.close()

    @staticmethod
    def change_password(user_id: int, previous_password: str,
                        new_password: str) -> None:
        if previous_password == new_password:
            raise ValueError("新密码不能与原密码相同。")

        if not re.match(PASSWORD_REGEX, new_password):
            raise ValueError("新密码格式错误。")

        user = UserService._get_user_by_id(user_id)
        if not check_password(previous_password, user.password):
            raise ValueError("原密码错误。")

        connection = get_connection()
        query = "UPDATE users SET password = %s WHERE user_id = %s"
        params = (hash_password(new_password), user_id)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise DatabaseError("修改密码失败") from e
        finally:
            connection.close()

    @staticmethod
    def follow(user_id: int, target_user_id: int) -> None:
        connection = get_connection()
        query = "INSERT INTO follows (follower_id, followee_id) VALUES (%s, %s)"
        params = (user_id, target_user_id)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise DatabaseError("关注失败") from e
        finally:
            connection.close()

    @staticmethod
    def unfollow(user_id: int, target_user_id: int) -> None:
        connection = get_connection()
        query = "DELETE FROM follows WHERE follower_id = %s AND followee_id = %s"
        params = (user_id, target_user_id)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise DatabaseError("取消关注失败") from e
        finally:
            connection.close()


class PostService:

    @staticmethod
    def create_post(user_id: int, content: str,
                    privacy_str: str = 'public') -> int:
        privacy = Privacy(privacy_str)

        if not privacy.is_valid():
            raise ValueError("隐私设置无效。")
        if not (0 < len(content) <= 500):
            raise ValueError("动态内容长度应在 1-500 字符之间。")

        connection = get_connection()
        query = \
            "INSERT INTO posts (user_id, content, privacy) " \
            "VALUES (%s, %s, %s) " \
            "RETURNING post_id"
        params = (user_id, content, privacy.privacy)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
                post = cursor.fetchone()
            connection.commit()
            return post['post_id']
        except Exception as e:
            connection.rollback()
            raise DatabaseError("发布动态失败") from e
        finally:
            connection.close()

    @staticmethod
    def get_post(user_id: int, post_id: int) -> Post:
        connection = get_connection()
        query = "CALL get_post(%s, %s);"
        params = (user_id, post_id)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
                post = cursor.fetchone()
            if not post:
                raise ValueError("动态不存在或不可见。")
            return Post(**post)
        except Exception as e:
            raise DatabaseError("获取动态失败") from e
        finally:
            connection.close()

    @staticmethod
    def get_posts(viewer_user_id: int | None = None,
                  target_user_id: int | None = None,
                  offset: int = 0, limit: int = PAGE_SIZE) -> list[Post]:
        connection = get_connection()
        query = "CALL get_visible_posts(%s, %s, %s, %s);"
        params = (viewer_user_id, target_user_id, offset, limit)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
                posts = cursor.fetchall()
            return [Post(**post) for post in posts]
        except Exception as e:
            raise DatabaseError("获取动态失败") from e
        finally:
            connection.close()

    @staticmethod
    def like(user_id: int, post_id: int) -> None:
        connection = get_connection()
        query = "INSERT INTO likes (user_id, post_id) VALUES (%s, %s);"
        params = (user_id, post_id)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise DatabaseError("点赞失败") from e
        finally:
            connection.close()

    @staticmethod
    def unlike(user_id: int, post_id: int) -> None:
        connection = get_connection()
        query = "DELETE FROM likes WHERE user_id = %s AND post_id = %s;"
        params = (user_id, post_id)

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, params)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise DatabaseError("取消点赞失败") from e
        finally:
            connection.close()
