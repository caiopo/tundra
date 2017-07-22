import pytest

from context import Graph, bfs, dfs, fringe, kruskal, prim


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
        tree = kruskal(g)


def test_dfs():
    g = Graph(range(10), zip(range(9), range(1, 10)))

    for i in range(10):
        r = dfs(g, 0, lambda v: v == i)

        assert r == i

    assert dfs(g, 0, lambda v: False) is None


def test_bfs():
    g = Graph(range(10), zip(range(9), range(1, 10)))

    for i in range(10):
        r = bfs(g, 0, lambda v: v == i)

        assert r == i

    assert bfs(g, 0, lambda v: False) is None


def test_fringe():
    g = Graph(range(10))

    g.link(0, 1)
    g.link(0, 2)
    g.link(0, 3)
    g.link(0, 4)

    g.link(1, 5)
    g.link(1, 6)
    g.link(1, 7)
    g.link(1, 8)

    g.link(2, 9)

    assert fringe(g, [0]) == set(range(1, 5))

    assert fringe(g, [1]) == {0} | set(range(5, 9))

    assert fringe(g, [2]) == {0, 9}

    assert fringe(g, [0, 1]) == set(range(2, 9))

    assert fringe(g, [0, 1, 2]) == g.vertices - {0, 1, 2}


def test_fringe_raises():
    g = Graph()

    with pytest.raises(ValueError):
        fringe(g, [0])
