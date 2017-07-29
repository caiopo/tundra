from typing import Dict, Hashable, Iterable, Set, Tuple, TypeVar, Union

__all__ = ('Digraph', 'Vertex', 'EdgeTuple')

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


class Digraph:
    def __init__(
        self,
        vertices: Iterable[Vertex] = (),
        edges: Iterable[EdgeTuple] = (),
    ) -> None:

        self._vertices: Dict[Vertex, Dict[Vertex, int]] = {}

        self.weight: Weight = Weight(self._vertices, False)

        for v in vertices:
            self.insert(v)

        for e in edges:
            self.link(*e)

    def insert(self, v: Vertex) -> None:
        """
        Adds the vertex v, if it doesn't exists
        """
        if v in self.vertices:
            raise KeyError(f'{v} is already a vertex')

        self._vertices[v] = {}

    def remove(self, v: Vertex) -> None:
        """
        Removes the vertex v, if it exists
        """
        for w in self.predecessors(v):
            self.unlink(w, v)

        for w in self.successors(v):
            self.unlink(v, w)

        del self._vertices[v]

    def link(self, v1: Vertex, v2: Vertex, weight: int = 1) -> None:
        """
        Adds the edge from the vertices v1 to v2, if it doesn't exists
        """
        if self.has_edge(v1, v2):
            raise ValueError(f'Edge ({v1}, {v2}) already exists')

        self._vertices[v1][v2] = weight

    def unlink(self, v1: Vertex, v2: Vertex) -> None:
        """
        Removes the edge from the vertices v1 to v2
        """
        if not self.has_edge(v1, v2):
            raise ValueError(f'Edge ({v1}, {v2}) does not exist')

        del self._vertices[v1][v2]

    def has_edge(self, v1: Vertex, v2: Vertex) -> bool:
        """
        Return True if there is an edge between v1 and v2, False otherwise
        """
        return v2 in self._vertices[v1]

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

    def degree(self, v: Vertex) -> int:
        """
        Returns the number of neighbors of v
        """
        return len(self.neighbors(v))

    @property
    def order(self) -> int:
        """
        Returns the number of vertices in the graph
        """
        return len(self._vertices)

    def __str__(self) -> str:
        return f'{type(self).__name__}({self.vertices}, {self.edges})'

    def __eq__(self, other) -> bool:
        return (
            isinstance(self, type(other)) and
            self.vertices == other.vertices and
            self.edges == other.edges
        )
