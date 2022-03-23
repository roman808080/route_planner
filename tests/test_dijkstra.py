from dijkstra import Graph, dijkstra_algorithm


def get_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    return " -> ".join(reversed(path))


def test_dijkstra_algorithm():
    nodes = ["Reykjavik", "Oslo", "Moscow", "London",
             "Rome", "Berlin", "Belgrade", "Athens"]

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
    previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node="Reykjavik")

    result = get_result(previous_nodes, shortest_path, start_node="Reykjavik", target_node="Belgrade")
    assert "Reykjavik -> Oslo -> Berlin -> Rome -> Athens -> Belgrade" == result
