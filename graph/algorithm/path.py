from math import inf
from typing import Dict, Set, Optional, List

from graph import Graph, Vertex


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
