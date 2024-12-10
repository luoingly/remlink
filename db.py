from config import get_db_config
import pymysql.cursors
import os


SCHEMA_SQL_FILE = os.path.join(
    os.path.dirname(__file__), 'sql', 'schema.sql')


def get_connection():
    return pymysql.connect(**get_db_config())


def init_db():
    assert os.path.exists(SCHEMA_SQL_FILE), \
        f"SQL file not found: {SCHEMA_SQL_FILE}"

    with open(SCHEMA_SQL_FILE, 'rt') as f:
        queries = [query for query in f.read().split(';') if query.strip()]

    connection = get_connection()
    with connection.cursor() as cursor:
        for query in queries:
            cursor.execute(query)
        connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
