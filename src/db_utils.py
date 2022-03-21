import os
from urllib.parse import quote_plus
from databases import Database


db_url = None
database = None


def get_db_settings(host='db', name='routes', port=5432,
                    user='admin', password='example'):
    host = os.environ.get('DB_HOST', host)
    name = os.environ.get('DB_NAME', name)

    port = int(os.environ.get('DB_PORT', port))
    user = quote_plus(str(os.environ.get('DB_USER', user)))
    password = quote_plus(str(os.environ.get('DB_PASSWORD', password)))

    return {'host': host, 'name': name, 'port': port, 'user': user,
            'password': password}


def create_db_url(host='db', name='routes', port=5432,
                  user='admin', password='example'):
    return f"postgresql+asyncpg://{user}:{password}@{host}:{str(port)}/{name}"


def create_database_connection(db_url, min_size=5, max_size=20):
    return Database(db_url, min_size=min_size, max_size=max_size)


def update_db_url(new_db_url):
    global db_url
    db_url = new_db_url


def update_database_connection(new_database):
    global database
    database = new_database


db_url = create_db_url(**get_db_settings())
database = create_database_connection(db_url=db_url)
