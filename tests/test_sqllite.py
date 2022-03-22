import pytest
from tempfile import NamedTemporaryFile
from sqlalchemy.ext.asyncio import create_async_engine

from db_utils import Db
from databases import Database
from schema import metadata, cities


async def test_sqllite_db():
    with NamedTemporaryFile() as temporary_db_file:
        db_url = 'sqlite+aiosqlite:///' + temporary_db_file.name
        db = Db(db_url=db_url)
        await db.up()

        temporary_db = db.get_database()

        tables_query = "SELECT * FROM sqlite_master where type='table';"
        tables = await temporary_db.fetch_all(query=tables_query)

        assert len(tables) != 0

        city_query = cities.insert(
            values={"name": 'London',
                    "lattitude": 51.509865,
                    "longitude": -0.118092})

        last_record_id = await temporary_db.execute(query=city_query)

        assert last_record_id == 1

        await temporary_db.disconnect()
