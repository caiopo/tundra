from random import choice
from typing import Set, Optional, Hashable as Vertex

class Graph:
    def __init__(self):
        self._vertices = {}

    def add_vertex(self, v: Vertex) -> None:
        """
        Adds the vertex v, if it is not there
        """
        if v in self.vertices():
            raise KeyError('{} is already a vertex'.format(v))

        self._vertices[v] = set()

    def remove_vertex(self, v: Vertex) -> None:
        """
        Removes the vertex v, if it is there
        """
        for v2 in self.neighbors(v):
            self.remove_edge(v, v2)

        del self._vertices[v]

    def add_edge(self, v1: Vertex, v2: Vertex) -> None:
        """
        Adds the edge from the vertices v1 to v2, if it is not there
        """
        self._vertices[v1].add(v2)
        self._vertices[v2].add(v1)

    def remove_edge(self, v1: Vertex, v2: Vertex) -> None:
        """
        Removes the edge from the vertices v1 to v2, if it is there
        """
        self._vertices[v1].remove(v2)
        if v1 != v2:
            self._vertices[v2].remove(v1)

    def order(self) -> int:
        """
        Returns the number of vertices in the graph
        """
        return len(self._vertices)

    def vertices(self) -> Set:
        """
        Returns a set containing the vertices of the graph
        """
        return set(self._vertices)

    def rand_vertex(self) -> Vertex:
        """
        Returns a random vertex of the graph
        """
        return choice(tuple(self.vertices()))

    def neighbors(self, v: Vertex) -> Set:
        """
        Returns a set containing the neighbors of v
        """
        return set(self._vertices[v])

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
