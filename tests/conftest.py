import pytest
from fastapi.testclient import TestClient
from tempfile import NamedTemporaryFile

from main import app


@pytest.fixture
async def client():
    return TestClient(app)


@pytest.fixture
async def temp_file():
    with NamedTemporaryFile() as temporary_file:
        yield temporary_file.name
