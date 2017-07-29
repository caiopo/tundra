from typing import Iterable, Set, Tuple

from .digraph import Digraph, EdgeTuple, Vertex, Weight

__all__ = ('Graph',)


class Graph(Digraph):
    def __init__(
        self,
        vertices: Iterable[Vertex] = (),
        edges: Iterable[EdgeTuple] = (),
    ) -> None:

        super().__init__(vertices)

        self.weight: Weight = Weight(self._vertices, True)

        for e in edges:
            self.link(*e)

    def link(self, v1: Vertex, v2: Vertex, weight: int = 1) -> None:
        """
        Adds the edge from the vertices v1 to v2, if it doesn't exists
        """
        super().link(v1, v2, weight)
        if v1 != v2:
            super().link(v2, v1, weight)

    def unlink(self, v1: Vertex, v2: Vertex) -> None:
        """
        Removes the edge from the vertices v1 to v2
        """
        super().unlink(v1, v2)
        if v1 != v2:
            super().unlink(v2, v1)

    @property
    def edges(self) -> Set[Tuple[Vertex, Vertex, int]]:
        """
        Returns a set containing the edges of the graph
        """
        return {
            (min(v1, v2), max(v1, v2), self.weight[v1, v2])
            for v1 in self.vertices
            for v2 in self.neighbors(v1)
        }

    def neighbors(self, v: Vertex) -> Set[Vertex]:
        """
        Returns a set containing the neighbors of v
        """
        return set(self._vertices[v].keys())
