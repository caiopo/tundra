from random import choice
from typing import Iterable, Tuple, Union, Dict, Set, Optional, Hashable as Vertex

class Graph:
    def __init__(self, vertices: Iterable[Vertex] = None,
        edges: Iterable[Tuple[Vertex, Vertex, Optional[int]]] = None) -> None:

        self._vertices = {} # type: Dict[Vertex, Dict[Vertex, int]]

        if vertices:
            for v in vertices:
                self.add_vertex(v)

        if edges:
            for e in edges:
                self.add_edge(*e)

    def add_vertex(self, v: Vertex) -> None:
        """
        Adds the vertex v, if it is not there
        """
        if v in self.vertices():
            raise KeyError('{} is already a vertex'.format(v))

        self._vertices[v] = {}

    def remove_vertex(self, v: Vertex) -> None:
        """
        Removes the vertex v, if it is there
        """
        for v2 in self.neighbors(v):
            self.remove_edge(v, v2)

        del self._vertices[v]

    def add_edge(self, v1: Vertex, v2: Vertex, weight: int = 1) -> None:
        """
        Adds the edge from the vertices v1 to v2, if it is not there
        """
        if v1 not in self.neighbors(v2):
            self._vertices[v1][v2] = weight
            self._vertices[v2][v1] = weight

    def remove_edge(self, v1: Vertex, v2: Vertex) -> None:
        """
        Removes the edge from the vertices v1 to v2, if it is there
        """
        del self._vertices[v1][v2]
        if v1 != v2:
            del self._vertices[v2][v1]

    def has_edge(self, v1: Vertex, v2: Vertex) -> bool:
        return v1 in self.neighbors(v2)

    def get_weight(self, v1: Vertex, v2: Vertex) -> int:
        """
        Returns the weight of the edge
        """
        return self._vertices[v1][v2]

    def set_weight(self, v1: Vertex, v2: Vertex, weight: int) -> None:
        """
        Sets the weight of the edge
        """
        self._vertices[v1][v2] = weight
        self._vertices[v2][v1] = weight

    def order(self) -> int:
        """
        Returns the number of vertices in the graph
        """
        return len(self._vertices)

    def vertices(self) -> Set[Vertex]:
        """
        Returns a set containing the vertices of the graph
        """
        return set(self._vertices)

    def edges(self) -> Set[Tuple[Vertex, Vertex, int]]:
        """
        Returns a set containing the edges of the graph
        """
        edges = set()

        for v1 in self.vertices():
            for v2 in self.neighbors(v1):
                edges.add((min(v1, v2), max(v1, v2), self.get_weight(v1, v2)))

        return edges

    def rand_vertex(self) -> Vertex:
        """
        Returns a random vertex of the graph
        """
        return choice(tuple(self.vertices()))

    def neighbors(self, v: Vertex) -> Set:
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
        degree = self.degree(self.rand_vertex())

        return all(self.degree(v) == degree for v in self.vertices())

    def is_complete(self) -> bool:
        """
        Return True if every vertex is connected to all other vertices,
        False otherwise
        """
        degree = self.order() - 1

        return all(self.degree(v) == degree for v in self.vertices())

    def is_connected(self) -> bool:
        """
        Return True if there is a path between every pair of vertices,
        False otherwise
        """
        return self.vertices() == self.transitive_closure(self.rand_vertex())

    def is_tree(self) -> bool:
        """
        Return True if the graph is connected and has no cycles, False otherwise
        """
        def cycle_with(v, v_prev, visited=None):
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
                    if cycle_with(v_neigh, v, visited):
                        return True

            visited.remove(v)

            return False

        v = self.rand_vertex()

        return self.is_connected() and not cycle_with(v, v)

    def transitive_closure(self, v: Vertex,
        visited: Optional[Set] = None) -> Set:
        """
        Returns a set containing all vertices reachable from v
        """
        visited = visited or set()

        visited.add(v)

        for v_neigh in self.neighbors(v):
            if not v_neigh in visited:
                self.transitive_closure(v_neigh, visited)

        return visited

    def __str__(self):
        return 'Graph({}, {})'.format(self.vertices(), self.edges())
