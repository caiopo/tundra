from typing import Dict

from graph import Graph, Vertex


def coloring(g: Graph) -> Dict[Vertex, int]:
    colors: Dict[Vertex, int] = {}

    for v in g.vertices:
        available = [True] * g.order

        for adj in g.neighbors(v):
            if colors.get(adj) is not None:
                available[colors[adj]] = False

        colors[v] = available.index(True)

    return colors
