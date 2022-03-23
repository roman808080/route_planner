import pytest

from dijkstra_adapter import DijkstraAdapter
from models import City, CityResponse, Road, RoadResponse
from db import get_city_id, get_city_name


def add_city_to_db(client, name):
    response = client.post("/city", json=City(name=name,
                                              lattitude=0, longitude=0).dict())
    city_response = CityResponse(**response.json())
    assert city_response.status == 'success'


def add_road_to_db(client, first_city, second_city, distance):
    road = Road(first_city_name=first_city, second_city_name=second_city,
                distance_km=distance, duration_minutes=1)
    response = client.post("/road", json=road.dict())

    road_response = RoadResponse(**response.json())
    assert road_response.status == 'success'


@pytest.fixture
async def prepared_database(client, sqlite_database):
    nodes = ["Reykjavik", "Oslo", "Moscow", "London",
             "Rome", "Berlin", "Belgrade", "Athens"]

    for node in nodes:
        add_city_to_db(client=client, name=node)

    add_road_to_db(client=client,
                   first_city="Reykjavik", second_city="Oslo",
                   distance=5)

    add_road_to_db(client=client,
                   first_city="Reykjavik", second_city="London",
                   distance=4)

    add_road_to_db(client=client,
                   first_city="Oslo", second_city="Berlin",
                   distance=1)

    add_road_to_db(client=client,
                   first_city="Oslo", second_city="Moscow",
                   distance=3)

    add_road_to_db(client=client,
                   first_city="Moscow", second_city="Belgrade",
                   distance=5)

    add_road_to_db(client=client,
                   first_city="Moscow", second_city="Athens",
                   distance=4)

    add_road_to_db(client=client,
                   first_city="Athens", second_city="Belgrade",
                   distance=1)

    add_road_to_db(client=client,
                   first_city="Rome", second_city="Berlin",
                   distance=2)

    add_road_to_db(client=client,
                   first_city="Rome", second_city="Athens",
                   distance=2)

    yield sqlite_database


async def test_dijkstra_algorithm(prepared_database):
    adapter = DijkstraAdapter(start_city='Reykjavik',
                              target_city='Belgrade', strategy='shortest')
    redable_path, shortest_path = await adapter.get_optimal_path()

    result = " -> ".join(redable_path)
    assert result == "Reykjavik -> Oslo -> Berlin -> Rome -> Athens -> Belgrade"

    assert shortest_path == 11
