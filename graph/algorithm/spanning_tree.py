from math import inf
from typing import Dict, cast

from graph import Graph, Vertex


def prim(g: Graph) -> Graph:
    """
    Constructs a minimum spanning tree using Prim's algorithm
    """
    cost: Dict[Vertex, float] = {v: inf for v in g.vertices}
    edge: Dict[Vertex, Vertex] = {v: None for v in g.vertices}

    tree = Graph()

    vertices_left = g.vertices

    while vertices_left:
        # find the vertex in the fringe with the minimal cost
        (current_vertex, current_cost), *_ = sorted(cost.items(),
                                                    key=lambda t: t[1])

        for v in g.neighbors(current_vertex):
            if v in cost and g.weight[v, current_vertex] < cost[v]:
                cost[v] = g.weight[v, current_vertex]
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

    The input graph must not have parallel edges or loops
    """
    for v1, v2, _ in g.edges:
        if v1 == v2:
            raise ValueError("g can't have loops")

    edges = sorted(g.edges, key=lambda e: e[2], reverse=True)

    t = Graph(g.vertices)

    n_edges = 0

    while t.order - 1 > n_edges:
        v1, v2, w = edges.pop()

        if v1 not in t.transitive_closure(v2):
            t.add_edge(v1, v2, w)
            n_edges += 1

    return t
