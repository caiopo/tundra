from typing import Dict, Iterable, Set

from tundra import Graph, Vertex

__all__ = ('fringe', 'coloring')


def fringe(g: Graph, selected: Iterable[Vertex]) -> Set[Vertex]:
    selected = set(selected)

    if not selected.issubset(g.vertices):
        raise ValueError("selected is not a subset of the graph's vertices")

    fr = set()

    for v in selected:
        for v2 in g.neighbors(v):
            if v2 not in selected:
                fr.add(v2)

    return fr


def coloring(g: Graph) -> Dict[Vertex, int]:
    colors: Dict[Vertex, int] = {}

    for v in g.vertices:
        available = [True] * g.order

        for adj in g.neighbors(v):
            if colors.get(adj) is not None:
                available[colors[adj]] = False

        colors[v] = available.index(True)

    return colors
