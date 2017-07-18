from random import choice
from typing import (Iterable, TypeVar, Union, Tuple,
                    Dict, Set, Optional, Hashable, Hashable as Vertex)

EdgeTuple = TypeVar('EdgeTuple', Tuple[Vertex, Vertex],
                    Tuple[Vertex, Vertex, int])


class Weight:
    def __init__(self, _vertices: Dict[Vertex, Dict[Vertex, int]]) -> None:
        self._vertices = _vertices

    def __getitem__(self, item: Tuple[Vertex, Vertex]) -> int:
        v1, v2 = item
        return self._vertices[v1][v2]

    def __setitem__(self, item: Tuple[Vertex, Vertex], weight: int):
        v1, v2 = item
        self._vertices[v1][v2] = weight
        self._vertices[v2][v1] = weight


class Graph:
    def __init__(self,
                 vertices: Iterable[Vertex] = (),
                 edges: Iterable[EdgeTuple] = ()) -> None:

        self._vertices: Dict[Vertex, Dict[Vertex, int]] = {}

        self.weight: Weight = Weight(self._vertices)

        for v in vertices:
            self.insert(v)

        for e in edges:
            self.link(*e)

    def insert(self, v: Vertex) -> None:
        """
        Adds the vertex v, if it doesn't exists
        """
        if v in self.vertices:
            raise KeyError('{} is already a vertex'.format(v))

        self._vertices[v] = {}

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
        if v1 not in self.neighbors(v2):
            self._vertices[v1][v2] = weight
            self._vertices[v2][v1] = weight

    def unlink(self, v1: Vertex, v2: Vertex) -> None:
        """
        Removes the edge from the vertices v1 to v2
        """
        del self._vertices[v1][v2]
        if v1 != v2:
            del self._vertices[v2][v1]

    def has_edge(self, v1: Vertex, v2: Vertex) -> bool:
        """
        Return True if there is an edge between v1 and v2, False otherwise
        """
        return v1 in self.neighbors(v2)

    @property
    def order(self) -> int:
        """
        Returns the number of vertices in the graph
        """
        return len(self._vertices)

    @property
    def vertices(self) -> Set[Vertex]:
        """
        Returns a set containing the vertices of the graph
        """
        return set(self._vertices)

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

    def degree(self, v: Vertex) -> int:
        """
        Returns the number of neighbors of v
        """
        return len(self.neighbors(v))

    def is_regular(self) -> bool:
        """
        Return True if all vertices have the same degree, False otherwise
        """
        degree = self.degree(self._random_vertex())

        return all(self.degree(v) == degree for v in self.vertices)

    def is_complete(self) -> bool:
        """
        Returns True if every vertex is connected to all other vertices,
        False otherwise
        """
        degree = self.order - 1

        return all(self.degree(v) == degree for v in self.vertices)

    def is_connected(self) -> bool:
        """
        Returns True if there is a path between every pair of vertices,
        False otherwise
        """
        return self.vertices == self.transitive_closure(self._random_vertex())

    def is_tree(self) -> bool:
        """
        Returns True if the graph is connected and has no cycles,
        False otherwise
        """
        v = self._random_vertex()

        return self.is_connected() and not self._cycle_with(v, v)

    def has_cycle(self) -> bool:
        """
        Returns True if there is a cycle in the graph, False otherwise
        """
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

    def _random_vertex(self) -> Vertex:
        """
        Returns a random vertex of the graph
        """
        return choice(tuple(self.vertices))

    def __str__(self) -> str:
        return f'Graph({self.vertices}, {self.edges})'
