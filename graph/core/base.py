from random import choice
from typing import (Dict, Hashable, Iterable, Optional, Set, Tuple, TypeVar,
                    Union)


Vertex = Union[Hashable, int]

EdgeTuple = TypeVar('EdgeTuple', Tuple[Vertex, Vertex],
                    Tuple[Vertex, Vertex, int])


class Weight:
    def __init__(
            self,
            _vertices: Dict[Vertex, Dict[Vertex, int]],
            symmetrical: bool,
    ) -> None:

        self._vertices = _vertices
        self._symmetrical = symmetrical

    def __getitem__(self, item: Tuple[Vertex, Vertex]) -> int:
        v1, v2 = item
        return self._vertices[v1][v2]

    def __setitem__(self, item: Tuple[Vertex, Vertex], weight: int):
        v1, v2 = item

        if v2 not in self._vertices[v1]:
            raise KeyError(
                f'{v1} and {v2} are not neighbors'
            )

        self._vertices[v1][v2] = weight

        if self._symmetrical:
            self._vertices[v2][v1] = weight


class BaseGraph:
    def __init__(
        self,
        vertices: Iterable[Vertex],
        symmetrical: bool,
    ) -> None:

        self._vertices: Dict[Vertex, Dict[Vertex, int]] = {}

        self.weight: Weight = Weight(self._vertices, symmetrical)

        for v in vertices:
            self.insert(v)

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
        raise NotImplementedError()

    def link(self, v1: Vertex, v2: Vertex, weight: int=1) -> None:
        """
        Adds the edge from the vertices v1 to v2, if it doesn't exists
        """
        raise NotImplementedError()

    def unlink(self, v1: Vertex, v2: Vertex) -> None:
        """
        Removes the edge from the vertices v1 to v2
        """
        raise NotImplementedError()

    def has_edge(self, v1: Vertex, v2: Vertex) -> bool:
        """
        Return True if there is an edge between v1 and v2, False otherwise
        """
        return v2 in self._vertices[v1]

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
        raise NotImplementedError()

    def neighbors(self, v: Vertex) -> Set[Vertex]:
        """
        Returns a set containing the neighbors of v
        """
        raise NotImplementedError()

    def degree(self, v: Vertex) -> int:
        """
        Returns the number of neighbors of v
        """
        return len(self.neighbors(v))

    def is_regular(self) -> bool:
        """
        Return True if all vertices have the same degree, False otherwise
        """
        if self.order == 0:
            return True

        degree = self.degree(self._random_vertex())

        return all(self.degree(v) == degree for v in self.vertices)

    def is_complete(self) -> bool:
        """
        Returns True if every vertex is connected to all other vertices,
        False otherwise
        """
        degree = self.order - 1

        return all(self.degree(v) == degree for v in self.vertices)

    def _random_vertex(self) -> Vertex:
        """
        Returns a random vertex of the graph
        """
        return choice(tuple(self.vertices))

    def __str__(self) -> str:
        return f'{type(self).__name__}({self.vertices}, {self.edges})'

    def __eq__(self, other) -> bool:
        return (
            isinstance(self, type(other)) and
            self.vertices == other.vertices and
            self.edges == other.edges
        )
