import re

from pymysql.cursors import DictCursor

from .utils import hash_password, check_password
from .db import get_connection, DatabaseError
from .model import User

USERNAME_REGEX = r'^[a-zA-Z0-9_]{4,20}$'
PASSWORD_REGEX = \
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$'


class UserService:

    @staticmethod
    def _get_user_by_username(username: str) -> User | None:
        assert re.match(USERNAME_REGEX, username)

        connection = get_connection()
        query = "SELECT * FROM users WHERE username = %s"

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, (username,))
                user = cursor.fetchone()
            return User(**user) if user else None
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

        try:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute(query, (username, hash_password(password)))
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
