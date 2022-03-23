from importlib.metadata import metadata
import os
from urllib.parse import quote_plus
from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from schema import metadata, cities, roads


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


async def is_in_table(query):
    database = db_manager.get_database()
    rows = await database.fetch_all(query=query)
    if len(rows) > 0:
        return True

    return False


async def is_city_in_table(name):
    query = cities.select().where(cities.c.name == name)
    return await is_in_table(query=query)


async def is_road_in_table(first_city_id, second_city_id):
    query = roads.select().where(roads.c.first_city_id == first_city_id,
                                 roads.c.second_city_id == second_city_id)
    return await is_in_table(query=query)


class DbManager:
    def __init__(self, db_url=None, db_settings={}, metadata=None):
        self.reset(db_url=db_url, db_settings=db_settings, metadata=metadata)

    def reset(self, db_url=None, db_settings={}, metadata=None):
        self._db_url = db_url
        self._db_settings = db_settings
        self._metadata = metadata

        self._database = None

        if self._db_url is None:
            self._db_url = create_db_url(**get_db_settings())

    async def _create_all_tables(self):
        async_engine = create_async_engine(self._db_url, echo=True)

        metadata_for_tables = None
        if self._metadata is None:
            metadata_for_tables = metadata

        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_for_tables.create_all)

    def _create_database(self):
        self._database = Database(self._db_url, **self._db_settings)

    async def up(self):
        await self._create_all_tables()
        self._create_database()
        await self._database.connect()

    async def down(self):
        if self._database is not None:
            await self._database.disconnect()
        self._database = None

    def get_database(self):
        if self._database is None:
            raise Exception('Database is not initialized.')
        return self._database


db_manager = DbManager()
