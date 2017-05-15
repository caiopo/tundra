from typing import Dict, cast
from graph import Graph, Vertex
from math import inf


def prim(g: Graph) -> Graph:
    """
    Constructs a minimum spanning tree using Prim's algorithm
    """
    cost = {v: inf for v in g.vertices}
    edge = {v: None for v in g.vertices}  # type: Dict[Vertex, Vertex]

    tree = Graph()

    vertices_left = g.vertices

    while vertices_left:
        # find the vertex in the fringe with the minimal cost
        current_vertex, current_cost = sorted(cost.items(),
                                              key=lambda t: t[1])[0]

        for v in g.neighbors(current_vertex):
            if v in cost and g.get_weight(v, current_vertex) < cost[v]:
                cost[v] = g.get_weight(v, current_vertex)
                edge[v] = current_vertex

        tree.add_vertex(current_vertex)

        if current_cost != inf:
            tree.add_edge(current_vertex, edge[current_vertex],
                          cast(int, current_cost))

        del edge[current_vertex]
        del cost[current_vertex]
        vertices_left.remove(current_vertex)

    return tree


def kruskal(g: Graph) -> Graph:
    """
    Constructs a minimum spanning tree using Kruskal's algorithm

    g must not have parallel edges or loops
    """
    edges = sorted(g.edges, key=lambda e: e[2], reverse=True)

    t = Graph(g.vertices)

    while not t.is_connected():
        v1, v2, w = edges.pop()

        if v1 not in t.transitive_closure(v2):
            t.add_edge(v1, v2, w)

    return t
