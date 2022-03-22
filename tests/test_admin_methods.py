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


async def test_delete_a_city(client, sqlite_database):
    await add_london(client=client)
    await check_amount_of_recrods_in_cities_is_1(sqlite_database=sqlite_database)

    response = client.delete("/city/London")

    city_response = CityResponse(**response.json())
    assert city_response.status == 'deleted'

    query = cities.select()
    rows = await sqlite_database.fetch_all(query=query)

    assert len(rows) == 0


async def test_delete_a_non_existing_city(client, sqlite_database):
    response = client.delete("/city/London")

    city_response = CityResponse(**response.json())
    assert city_response.status == 'deleted'

    query = cities.select()
    rows = await sqlite_database.fetch_all(query=query)

    assert len(rows) == 0


async def test_update_a_city(client, sqlite_database):
    await add_london(client=client)
    await check_amount_of_recrods_in_cities_is_1(sqlite_database=sqlite_database)

    updated_london = City(name="London", lattitude=0, longitude=0)
    response = client.put("/city/London", json=updated_london.dict())

    city_response = CityResponse(**response.json())
    assert city_response.status == 'updated'

    query = cities.select().where(cities.c.name == 'London')
    row = await sqlite_database.fetch_one(query=query)

    assert row['lattitude'] == 0
    assert row['longitude'] == 0


async def test_update_a_city_which_does_not_exist(client, sqlite_database):
    updated_london = City(name="London", lattitude=0, longitude=0)
    response = client.put("/city/London", json=updated_london.dict())

    assert response.status_code == 404
    assert response.json()['detail'] == 'Item not found'
