import pymysql

from pymysql.connections import Connection
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from pathlib import Path

from .config import get_db_config


SCHEMA_SQL_FILE = Path(__file__).parent.parent / 'sql' / 'schema.sql'
VIEW_SQL_FILE = Path(__file__).parent.parent / 'sql' / 'view.sql'
PROCEDURE_SQL_FILE = Path(__file__).parent.parent / 'sql' / 'procedure.sql'


pool = None


class DatabaseError(Exception):
    def __init__(self, message: str):
        super().__init__(f"数据库错误，{message}。")


def init_pool():
    global pool
    config = get_db_config()
    pool = PooledDB(creator=pymysql, **config)


def get_connection() -> Connection:
    if pool is None:
        init_pool()
    return pool.connection()


def init_db():

    queries = []
    for file in [SCHEMA_SQL_FILE, VIEW_SQL_FILE, PROCEDURE_SQL_FILE]:
        assert file.exists(), f"SQL file not exists: {file}"
        with open(file, 'rt', encoding='utf-8') as f:
            queries.extend(
                [query for query in f.read().split('\n\n\n') if query.strip()])

    connection = get_connection()
    with connection.cursor(DictCursor) as cursor:
        for query in queries:
            cursor.execute(query)
        connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
