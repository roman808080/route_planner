import pytest
from models import City, CityResponse
from schema import cities


async def add_london(client):
    response = client.post("/city", json=City(name="London",
                           lattitude=51.509865, longitude=-0.118092).dict())

    city_response = CityResponse(**response.json())
    assert city_response.status == 'success'


async def check_amount_of_recrods_in_cities_is_1(sqlite_database):
    query = cities.select()
    rows = await sqlite_database.fetch_all(query=query)

    assert len(rows) == 1


async def test_add_city(client, sqlite_database):
    await add_london(client=client)
    await check_amount_of_recrods_in_cities_is_1(sqlite_database=sqlite_database)



async def test_adding_the_same_city_two_times(client, sqlite_database):
    await add_london(client=client)
    await add_london(client=client)
    await check_amount_of_recrods_in_cities_is_1(sqlite_database=sqlite_database)
