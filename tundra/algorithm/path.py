from math import inf
from typing import Dict, List, Optional, Set, Tuple

from tundra import Graph, Vertex

__all__ = ('shortest_distance', 'dijkstra', 'floyd_warshall')


def _dijkstra(g: Graph, start: Vertex):
    distance = {v: inf for v in g.vertices}
    distance[start] = 0

    previous: Dict[Vertex, Optional[Vertex]]
    previous = {v: None for v in g.vertices}

    unvisited: Set[Vertex] = g.vertices

    while len(unvisited) > 0:
        (current, _), *__ = sorted({(v, distance[v]) for v in unvisited},
                                   key=lambda t: t[1])

        unvisited.remove(current)

        for n in g.neighbors(current):
            distn = distance[current] + g.weight[current, n]

            if distn < distance[n]:
                distance[n] = distn
                previous[n] = current

    return distance, previous


def shortest_distance(g: Graph, start: Vertex) -> Dict[Vertex, float]:
    distance, _ = _dijkstra(g, start)

    return distance


def dijkstra(g: Graph, start: Vertex, end: Vertex) -> List[Vertex]:
    _, previous = _dijkstra(g, start)

    path: List[Vertex] = []

    current = end

    while previous[current] is not None:
        path.append(current)

        current = previous[current]

    path.append(current)

    return list(reversed(path))


def floyd_warshall(g: Graph) -> Dict[Vertex, Dict[Vertex, float]]:
    dist: Dict[Vertex, Dict[Vertex, float]] = {}

    vertices = g.vertices

    for v1 in vertices:
        dist[v1] = {}

        for v2 in vertices:
            if v1 is v2:
                dist[v1][v2] = 0
            elif g.has_edge(v1, v2):
                dist[v1][v2] = g.weight[v1, v2]
            else:
                dist[v1][v2] = inf

    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist
