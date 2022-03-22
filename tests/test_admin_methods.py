import pytest
from models import City, CityResponse
from schema import cities


async def test_add_city(client, sqlite_database):
    response = client.post("/city", json=City(name="London",
                           lattitude=51.509865, longitude=-0.118092).dict())

    city_response = CityResponse(**response.json())
    assert city_response.status == 'success'

    query = cities.select()
    rows = await sqlite_database.fetch_all(query=query)

    assert len(rows) == 1
