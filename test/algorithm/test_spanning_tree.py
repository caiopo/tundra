import pytest

from context import Graph, kruskal, prim


def test_prim():
    g = Graph(range(10))

    for v in g.vertices:
        if v != 0:
            g.link(0, v, 5)

    for v1 in g.vertices:
        for v2 in g.vertices:
            if v1 != v2 and not g.has_edge(v1, v2):
                g.link(v1, v2, 10)

    tree = prim(g)

    assert tree.vertices == set(range(10))

    assert tree.edges == {(0, i, 5) for i in range(1, 10)}


def test_kruskal():
    g = Graph(range(10))

    for v in g.vertices:
        if v != 0:
            g.link(0, v, 5)

    for v1 in g.vertices:
        for v2 in g.vertices:
            if v1 != v2 and not g.has_edge(v1, v2):
                g.link(v1, v2, 10)

    tree = kruskal(g)

    assert tree.vertices == set(range(10))

    assert tree.edges == {(0, i, 5) for i in range(1, 10)}


def test_kruskal_raises():
    g = Graph(range(10))

    for v in g.vertices:
        g.link(0, v, 5)

    for v1 in g.vertices:
        for v2 in g.vertices:
            if v1 != v2 and not g.has_edge(v1, v2):
                g.link(v1, v2, 10)

    with pytest.raises(ValueError):
        kruskal(g)
