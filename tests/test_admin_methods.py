import pytest
from models import City


async def test_add_city(client, sqlite_database):
    response = client.post("/city", json=City(name="London",
                           lattitude=51.509865, longitude=-0.118092).dict())
    assert response.json()['id'] == 1
