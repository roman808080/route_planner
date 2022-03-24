import pytest
from fastapi.testclient import TestClient
from tempfile import NamedTemporaryFile

from main import app
from db import db_manager
from test_utils import add_city_to_db, add_road_to_db


@pytest.fixture
async def client():
    return TestClient(app)


@pytest.fixture
async def temp_file():
    with NamedTemporaryFile() as temporary_file:
        yield temporary_file.name


class DbManagerGuard:
    def __init__(self, db_manager, db_url):
        self._db_manager = db_manager
        self._db_manager.reset(db_url=db_url)

    async def __aenter__(self):
        await self._db_manager.up()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._db_manager.down()
        self._db_manager.reset()


@pytest.fixture
async def sqlite_database(temp_file):
    db_url = 'sqlite+aiosqlite:///' + temp_file
    async with DbManagerGuard(db_manager=db_manager, db_url=db_url):
        yield db_manager.get_database()


@pytest.fixture
async def prepared_database(client, sqlite_database):
    nodes = ["Reykjavik", "Oslo", "Moscow", "London",
             "Rome", "Berlin", "Belgrade", "Athens"]

    for node in nodes:
        add_city_to_db(client=client, name=node)

    add_road_to_db(client=client,
                   first_city="Reykjavik", second_city="Oslo",
                   distance=5,
                   duration=3)

    add_road_to_db(client=client,
                   first_city="Reykjavik", second_city="London",
                   distance=4,
                   duration=5)

    add_road_to_db(client=client,
                   first_city="Oslo", second_city="Berlin",
                   distance=1,
                   duration=2)

    add_road_to_db(client=client,
                   first_city="Oslo", second_city="Moscow",
                   distance=3,
                   duration=4)

    add_road_to_db(client=client,
                   first_city="Moscow", second_city="Belgrade",
                   distance=5,
                   duration=1)

    add_road_to_db(client=client,
                   first_city="Moscow", second_city="Athens",
                   distance=4,
                   duration=2)

    add_road_to_db(client=client,
                   first_city="Athens", second_city="Belgrade",
                   distance=1,
                   duration=1)

    add_road_to_db(client=client,
                   first_city="Rome", second_city="Berlin",
                   distance=2,
                   duration=3)

    add_road_to_db(client=client,
                   first_city="Rome", second_city="Athens",
                   distance=2,
                   duration=2)

    yield sqlite_database
