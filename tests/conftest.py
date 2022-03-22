import pytest
from fastapi.testclient import TestClient
from tempfile import NamedTemporaryFile

from main import app
from db import db_manager


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
