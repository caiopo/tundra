from typing import Iterable, Optional, Set, Tuple

from .base import BaseGraph, Vertex, EdgeTuple


class Graph(BaseGraph):
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
        for v2 in self.neighbors(v):
            self.unlink(v, v2)

        del self._vertices[v]

    def link(self, v1: Vertex, v2: Vertex, weight: int = 1) -> None:
        """
        Adds the edge from the vertices v1 to v2, if it doesn't exists
        """
        if not self.has_edge(v1, v2):
            self._vertices[v1][v2] = weight
            self._vertices[v2][v1] = weight

    def unlink(self, v1: Vertex, v2: Vertex) -> None:
        """
        Removes the edge from the vertices v1 to v2
        """
        del self._vertices[v1][v2]

        if v1 != v2:
            del self._vertices[v2][v1]

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

    def is_connected(self) -> bool:
        """
        Returns True if there is a path between every pair of vertices,
        False otherwise
        """
        if self.order == 0:
            return True

        return self.vertices == self.transitive_closure(self._random_vertex())

    def is_tree(self) -> bool:
        """
        Returns True if the graph is connected and has no cycles,
        False otherwise
        """
        if self.order == 0:
            return False

        v = self._random_vertex()

        return self.is_connected() and not self._cycle_with(v, v)

    def has_cycle(self) -> bool:
        """
        Returns True if there is a cycle in the graph, False otherwise
        """
        if self.order == 0:
            return False

        v = self._random_vertex()

        return self._cycle_with(v, v)

    def transitive_closure(
            self, v: Vertex,
            visited: Optional[Set[Vertex]] = None) -> Set[Vertex]:
        """
        Returns a set containing all vertices reachable from v
        """
        visited = visited or set()

        visited.add(v)

        for v_neigh in self.neighbors(v):
            if v_neigh not in visited:
                self.transitive_closure(v_neigh, visited)

        return visited

    def _cycle_with(self, v, v_prev, visited=None):
        """
        Returns True if there is a cycle in the graph containing v,
        False otherwise
        """
        visited = visited or set()

        if v in visited:
            return True

        visited.add(v)

        for v_neigh in self.neighbors(v):
            if v_neigh != v_prev:
                if self._cycle_with(v_neigh, v, visited):
                    return True

        visited.remove(v)

        return False
