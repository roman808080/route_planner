from dijkstra import Graph, dijkstra_algorithm
from db import get_city_id, get_city_ids, db_manager, get_city_name, get_sum_of_parameters_for_path
from schema import cities, roads
from models import PlanningStrategy


class NonExistingNode(Exception):
    pass


class RouteDoesNotExist(Exception):
    pass


class DijkstraAdapter:
    _strategy_map = {
        PlanningStrategy.shortest: 'distance_km',
        PlanningStrategy.fastest: 'duration_minutes',
    }

    def __init__(self, start_city, target_city, strategy):
        self._start_city = start_city
        self._target_city = target_city
        self._strategy = strategy

        self._strategy_attr = DijkstraAdapter._strategy_map[strategy]

    async def get_optimal_path(self):
        if self._start_city == self._target_city:
            return ([], 0, 0)

        nodes = await get_city_ids()
        init_graph = await self._get_init_graph()

        start_node = await get_city_id(name=self._start_city)
        target_node = await get_city_id(name=self._target_city)

        if None in [start_node, target_node]:
            self._raise_non_existing_node_exception(start_node=start_node,
                                                    target_node=target_node)

        graph = Graph(nodes, init_graph)
        previous_nodes, _ = dijkstra_algorithm(graph=graph,
                                               start_node=start_node)

        if len(previous_nodes) == 0:
            self._raise_route_does_not_exist(start_node=start_node,
                                             target_node=target_node)

        built_path = list(DijkstraAdapter._build_path(previous_nodes=previous_nodes,
                                                      start_node=start_node, target_node=target_node))

        duration, distance = await get_sum_of_parameters_for_path(built_path)
        readable_path = await DijkstraAdapter._convert_built_path_to_readable(built_path=built_path)

        return (readable_path, duration, distance)

    def _raise_non_existing_node_exception(self, start_node, target_node):
        message = (f'One of the nodes does not exist. '
                   f'Start city = {self._start_city}, target city = {self._target_city}. '
                   f'Start node = {start_node}, target node = {target_node}')
        raise NonExistingNode(message)

    def _raise_route_does_not_exist(self, start_node, target_node):
        message = (f'The route does not exist. '
                   f'Start city = {self._start_city}, target city = {self._target_city}. '
                   f'Start node = {start_node}, target node = {target_node}')
        raise RouteDoesNotExist(message)

    @staticmethod
    def _build_path(previous_nodes, start_node, target_node):
        path = []
        node = target_node

        while node != start_node:
            path.append(node)
            node = previous_nodes[node]

        # Add the start node manually
        path.append(start_node)

        return reversed(path)

    @staticmethod
    async def _convert_built_path_to_readable(built_path):
        readable_nodes = []
        for node in built_path:
            readable_nodes.append(await get_city_name(city_id=node))

        return readable_nodes

    async def _get_init_graph(self):
        init_graph = {}

        query = cities.select()
        database = db_manager.get_database()
        rows = await database.fetch_all(query=query)

        for row in rows:
            init_graph[row.id] = {}

        query = roads.select()
        rows = await database.fetch_all(query=query)

        for row in rows:
            init_graph[row.first_city_id][row.second_city_id] = getattr(
                row, self._strategy_attr)

        return init_graph
