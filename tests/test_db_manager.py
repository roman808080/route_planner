import pytest

from db import db_manager
from schema import cities


async def test_reset(sqlite_database):
    tables_query = "SELECT * FROM sqlite_master where type='table';"
    tables = await sqlite_database.fetch_all(query=tables_query)

    assert len(tables) != 0

    city_query = cities.insert(
        values={"name": 'London',
                "lattitude": 51.509865,
                "longitude": -0.118092})

    last_record_id = await sqlite_database.execute(query=city_query)
    assert last_record_id == 1
