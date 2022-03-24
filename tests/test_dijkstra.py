import pytest

from test_utils import add_city_to_db
from dijkstra_adapter import DijkstraAdapter, NonExistingNode, RouteDoesNotExist
from models import PlanningStrategy


async def test_dijkstra_algorithm_shortest(prepared_database):
    adapter = DijkstraAdapter(start_city='Reykjavik',
                              target_city='Belgrade', strategy=PlanningStrategy.shortest)
    readable_path, distance, duration = await adapter.get_optimal_path()

    result = " -> ".join(readable_path)
    assert result == "Reykjavik -> Oslo -> Berlin -> Rome -> Athens -> Belgrade"

    assert distance == 11
    assert duration == 11


async def test_dijkstra_algorithm_fastest(prepared_database):
    adapter = DijkstraAdapter(start_city='Reykjavik',
                              target_city='Belgrade', strategy=PlanningStrategy.fastest)
    readable_path, distance, duration = await adapter.get_optimal_path()

    result = " -> ".join(readable_path)
    assert result == "Reykjavik -> Oslo -> Moscow -> Belgrade"

    assert distance == 13
    assert duration == 8


async def test_simple_road(prepared_database):
    adapter = DijkstraAdapter(start_city='Reykjavik',
                              target_city='Oslo', strategy=PlanningStrategy.fastest)
    readable_path, distance, duration = await adapter.get_optimal_path()

    assert readable_path == ['Reykjavik', 'Oslo']
    assert distance == 5
    assert duration == 3


async def test_non_existing_start(prepared_database):
    with pytest.raises(NonExistingNode) as exc:
        adapter = DijkstraAdapter(start_city='Dnipro',
                                  target_city='Oslo', strategy=PlanningStrategy.fastest)
        _, _, _ = await adapter.get_optimal_path()

    expected_message = ("One of the nodes does not exist. "
                        "Start city = Dnipro, target city = Oslo. Start node = None, target node = 2")
    assert expected_message == str(exc.value)


async def test_non_existing_road(client, prepared_database):
    add_city_to_db(client=client, name='Druzhkivka')

    with pytest.raises(RouteDoesNotExist) as exc:
        adapter = DijkstraAdapter(start_city='Druzhkivka',
                                    target_city='Oslo', strategy=PlanningStrategy.fastest)
        _, _, _= await adapter.get_optimal_path()

    expected_message = ("The route does not exist. "
                        "Start city = Druzhkivka, target city = Oslo.")
    assert expected_message in str(exc.value)
