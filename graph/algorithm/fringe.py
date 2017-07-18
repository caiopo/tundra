from typing import Hashable as Vertex
from typing import Iterable, Set

from graph import Graph


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
