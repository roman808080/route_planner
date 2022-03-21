import os
import urllib.parse

from databases import Database

# Get env variables for db connection
db_host = os.environ.get('db_host', 'db')
db_name = os.environ.get('db_name', 'routes')
db_port = urllib.parse.quote_plus(str(os.environ.get('db_port', '5432')))
db_user = urllib.parse.quote_plus(str(os.environ.get('db_user', 'admin')))
db_pass = urllib.parse.quote_plus(str(os.environ.get('db_pass', 'example')))

db_url = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

database: Database = Database(db_url,
                              min_size=5,
                              max_size=20)
