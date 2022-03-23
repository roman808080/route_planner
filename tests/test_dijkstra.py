from dijkstra import Graph, dijkstra_algorithm
from models import City, CityResponse, Road, RoadResponse


def get_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    return " -> ".join(reversed(path))


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


def test_dijkstra_algorithm(client, sqlite_database):
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

    init_graph = {}
    for node in nodes:
        init_graph[node] = {}

    init_graph["Reykjavik"]["Oslo"] = 5
    init_graph["Reykjavik"]["London"] = 4
    init_graph["Oslo"]["Berlin"] = 1
    init_graph["Oslo"]["Moscow"] = 3
    init_graph["Moscow"]["Belgrade"] = 5
    init_graph["Moscow"]["Athens"] = 4
    init_graph["Athens"]["Belgrade"] = 1
    init_graph["Rome"]["Berlin"] = 2
    init_graph["Rome"]["Athens"] = 2

    graph = Graph(nodes, init_graph)
    previous_nodes, shortest_path = dijkstra_algorithm(
        graph=graph, start_node="Reykjavik")

    result = get_result(previous_nodes, shortest_path,
                        start_node="Reykjavik", target_node="Belgrade")
    assert "Reykjavik -> Oslo -> Berlin -> Rome -> Athens -> Belgrade" == result
