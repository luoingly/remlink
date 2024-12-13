import os

from secrets import token_urlsafe
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path


ENV_FILEPATH = Path(__file__).parent.parent / '.env'

DEFAULT_DB_CONFIG = {
    'maxconnections': 10,
    'mincached': 2,
    'blocking': True,
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'remlink',
    'charset': 'utf8'
}


if ENV_FILEPATH.exists():
    load_dotenv(ENV_FILEPATH)


def get_db_config() -> dict:

    config = DEFAULT_DB_CONFIG.copy()
    config['host'] = os.getenv('DB_HOST', config['host'])
    config['user'] = os.getenv('DB_USER', config['user'])
    config['password'] = os.getenv('DB_PASSWORD', config['password'])
    config['database'] = os.getenv('DB_DATABASE', config['database'])

    return config


def get_secret_key() -> str:
    return os.getenv('SECRET_KEY', token_urlsafe(16))


def is_debug_enabled() -> bool:
    return os.getenv('DEBUG', 'False').lower() == 'true'

def get_timezone() -> timedelta:
    return timedelta(hours=int(os.getenv('TIMEZONE', 0)))


if __name__ == '__main__':
    for key, value in get_db_config().items():
        print(f'{key}: {value}')
