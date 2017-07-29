from random import choice
from typing import Optional, Set

from tundra import Digraph, Graph, Vertex

__all__ = ('is_tree', 'is_regular', 'is_complete',
           'is_connected', 'has_cycle', 'transitive_closure')


def _random_vertex(g: Digraph) -> Vertex:
    """
    Returns a random vertex of the graph
    """
    return choice(tuple(g.vertices))


def is_regular(g: Digraph) -> bool:
    """
    Return True if all vertices have the same degree, False otherwise
    """
    if g.order == 0:
        return True

    degree = g.degree(_random_vertex(g))

    return all(g.degree(v) == degree for v in g.vertices)


def is_complete(g: Digraph) -> bool:
    """
    Returns True if every vertex is connected to all other vertices,
    False otherwise
    """
    degree = g.order - 1

    return all(g.degree(v) == degree for v in g.vertices)


def is_connected(g: Graph) -> bool:
    """
    Returns True if there is a path between every pair of vertices,
    False otherwise
    """
    if g.order == 0:
        return True

    return g.vertices == transitive_closure(g, _random_vertex(g))


def is_tree(g: Graph) -> bool:
    """
    Returns True if the graph is connected and has no cycles,
    False otherwise
    """
    if g.order == 0:
        return False

    v = _random_vertex(g)

    return is_connected(g) and not _cycle_with(g, v, v)


def has_cycle(g: Graph) -> bool:
    """
    Returns True if there is a cycle in the graph, False otherwise
    """
    if g.order == 0:
        return False

    v = _random_vertex(g)

    return _cycle_with(g, v, v)


def transitive_closure(
        g: Graph,
        v: Vertex,
        visited: Optional[Set[Vertex]] = None) -> Set[Vertex]:
    """
    Returns a set containing all vertices reachable from v
    """
    visited = visited or set()

    visited.add(v)

    for v_neigh in g.neighbors(v):
        if v_neigh not in visited:
            transitive_closure(g, v_neigh, visited)

    return visited


def _cycle_with(
        g: Graph,
        v: Vertex,
        v_prev: Vertex,
        visited: Set[Vertex]=None
) -> bool:
    """
    Returns True if there is a cycle in the graph containing v,
    False otherwise
    """
    visited = visited or set()

    if v in visited:
        return True

    visited.add(v)

    for v_neigh in g.neighbors(v):
        if v_neigh != v_prev:
            if _cycle_with(g, v_neigh, v, visited):
                return True

    visited.remove(v)

    return False
