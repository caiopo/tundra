from typing import Iterable, Optional, Set, Tuple

from .base import BaseGraph, Vertex, EdgeTuple


class Digraph(BaseGraph):
    def __init__(
        self,
        vertices: Iterable[Vertex] = (),
        edges: Iterable[EdgeTuple] = ()
    ) -> None:

        super().__init__(vertices, True)

        for e in edges:
            self.link(*e)

    def remove(self, v: Vertex) -> None:
        """
        Removes the vertex v, if it exists
        """

    def link(self, v1: Vertex, v2: Vertex, weight: int = 1) -> None:
        """
        Adds the edge from the vertices v1 to v2, if it doesn't exists
        """
        if not self.has_edge(v1, v2):
            self._vertices[v1][v2] = weight

    def unlink(self, v1: Vertex, v2: Vertex) -> None:
        """
        Removes the edge from the vertices v1 to v2
        """
        del self._vertices[v1][v2]

    @property
    def edges(self) -> Set[Tuple[Vertex, Vertex, int]]:
        """
        Returns a set containing the edges of the graph
        """
        return {
            (v1, v2, self.weight[v1, v2])
            for v1 in self.vertices
            for v2 in self.successors(v1)
        }

    def predecessors(self, v: Vertex) -> Set[Vertex]:
        return {w for w in self.vertices if self.has_edge(w, v)}

    def successors(self, v: Vertex) -> Set[Vertex]:
        return set(self._vertices[v])

    def neighbors(self, v: Vertex) -> Set[Vertex]:
        """
        Returns a set containing the neighbors of v
        """
        return self.predecessors(v) | self.successors(v)

    def indegree(self, v: Vertex) -> int:
        return len(self.predecessors(v))

    def outdegree(self, v: Vertex) -> int:
        return len(self.successors(v))
