from dijkstra_adapter import DijkstraAdapter
from models import PlanningStrategy


async def test_dijkstra_algorithm_shortest(prepared_database):
    adapter = DijkstraAdapter(start_city='Reykjavik',
                              target_city='Belgrade', strategy=PlanningStrategy.shortest)
    # redable_path, shortest_path = await adapter.get_optimal_path()
    redable_path, distance, duration = await adapter.get_optimal_path()

    result = " -> ".join(redable_path)
    assert result == "Reykjavik -> Oslo -> Berlin -> Rome -> Athens -> Belgrade"

    assert distance == 11
    assert duration == 11


async def test_dijkstra_algorithm_fastest(prepared_database):
    adapter = DijkstraAdapter(start_city='Reykjavik',
                              target_city='Belgrade', strategy=PlanningStrategy.fastest)
    # redable_path, shortest_path = await adapter.get_optimal_path()
    redable_path, distance, duration = await adapter.get_optimal_path()

    result = " -> ".join(redable_path)
    assert result == "Reykjavik -> Oslo -> Moscow -> Belgrade"

    assert distance == 13
    assert duration == 8
