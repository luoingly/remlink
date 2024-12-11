from dotenv import load_dotenv
from pathlib import Path
import pymysql.cursors
import os

ENV_FILEPATH = Path(__file__).parent.parent / '.env'

DEFAULT_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'remlink',
    'cursorclass': pymysql.cursors.DictCursor
}


def get_db_config():
    if ENV_FILEPATH.exists():
        load_dotenv(ENV_FILEPATH)

    config = DEFAULT_DB_CONFIG.copy()
    config['host'] = os.getenv('DB_HOST', config['host'])
    config['user'] = os.getenv('DB_USER', config['user'])
    config['password'] = os.getenv('DB_PASSWORD', config['password'])
    config['database'] = os.getenv('DB_DATABASE', config['database'])

    return config


if __name__ == '__main__':
    for key, value in get_db_config().items():
        print(f'{key}: {value}')