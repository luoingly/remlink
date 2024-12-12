import pymysql

from pymysql.connections import Connection
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from .config import get_db_config
from pathlib import Path


SCHEMA_SQL_FILE = Path(__file__).parent.parent / 'sql' / 'schema.sql'


pool = None


def init_pool():
    global pool
    config = get_db_config()
    pool = PooledDB(creator=pymysql, **config)


def get_connection() -> Connection:
    if pool is None:
        init_pool()
    return pool.connection()


def init_db():

    assert SCHEMA_SQL_FILE.exists(), \
        f"SQL file not found: {SCHEMA_SQL_FILE}"

    with open(SCHEMA_SQL_FILE, 'rt') as f:
        queries = [query for query in f.read().split(';') if query.strip()]

    connection = get_connection()
    with connection.cursor(DictCursor) as cursor:
        for query in queries:
            cursor.execute(query)
        connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
