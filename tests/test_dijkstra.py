from dijkstra import Graph, dijkstra_algorithm
from models import City, CityResponse, Road, RoadResponse
from db import get_city_id, db_manager
from schema import cities, roads


async def get_city_name(city_id: int):
    """Get a city name"""
    query = cities.select().where(cities.c.id == city_id)

    database = db_manager.get_database()
    row = await database.fetch_one(query=query)

    if row is None:
        return None

    return row.name


async def convert_nodes_to_readable(nodes):
    readable_nodes = []
    for node in nodes:
        readable_nodes.append(await get_city_name(city_id=node))
    
    return readable_nodes


def get_shortest_path_for_target_node(shortest_paths, target_node):
    return shortest_paths[target_node]

def get_path(previous_nodes, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    return reversed(path)


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


async def convert_nodes(nodes):
    id_nodes = []
    for node in nodes:
        id_nodes.append(await get_city_id(name=node))

    return id_nodes


async def get_init_graph(database):
    init_graph = {}

    query = cities.select()
    rows = await database.fetch_all(query=query)

    for row in rows:
        init_graph[row.id] = {}

    query = roads.select()
    rows = await database.fetch_all(query=query)

    for row in rows:
        init_graph[row.first_city_id][row.second_city_id] = row.distance_km

    return init_graph


async def test_dijkstra_algorithm(client, sqlite_database):
    nodes = ["Reykjavik", "Oslo", "Moscow", "London",
             "Rome", "Berlin", "Belgrade", "Athens"]

    for node in nodes:
        add_city_to_db(client=client, name=node)

    converted_nodes = await convert_nodes(nodes=nodes)

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

    init_graph = await get_init_graph(database=sqlite_database)
    start_node = await get_city_id(name="Reykjavik")
    target_node = await get_city_id(name="Belgrade")

    graph = Graph(converted_nodes, init_graph)
    previous_nodes, shortest_paths = dijkstra_algorithm(graph=graph,
                                                       start_node=start_node)

    node_path = get_path(previous_nodes, start_node=start_node, target_node=target_node)
    
    readable_path = await convert_nodes_to_readable(node_path)
    result = " -> ".join(readable_path)

    assert get_shortest_path_for_target_node(shortest_paths, target_node) == 11
    assert "Reykjavik -> Oslo -> Berlin -> Rome -> Athens -> Belgrade" == result
