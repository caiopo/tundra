import pytest

from context import (Graph, has_cycle, is_complete, is_connected, is_regular,
                     is_tree, transitive_closure)

MAX = 100


@pytest.fixture
def g():
    return Graph(range(MAX))


def test_regular(g):
    assert is_regular(Graph())

    assert is_regular(g)

    g.link(0, 1)

    assert not is_regular(g)

    for i in range(1, MAX):
        g.link(i, (i + 1) % MAX)

    assert is_regular(g)

    g.link(1, 3)

    assert not is_regular(g)


def test_complete(g):
    assert not is_complete(g)

    for i in range(MAX):
        for j in range(MAX):
            if not g.has_edge(i, j):
                g.link(i, j)

    assert not is_complete(g)

    for i in range(MAX):
        g.unlink(i, i)

    assert is_complete(g)


def test_connected(g):
    assert is_connected(Graph())

    assert not is_connected(g)

    for i in range(0, MAX, 2):
        g.link(i, i + 1)

    assert not is_connected(g)

    for i in range(1, MAX, 2):
        g.link(i, (i + 1) % MAX)

    assert is_connected(g)


def test_tree_true(g):
    for i in range(MAX):
        if (2 * i + 1) < MAX:
            g.link(i, 2 * i + 1)

        if (2 * i + 2) < MAX:
            g.link(i, 2 * i + 2)

    assert is_tree(g)


def test_tree_false(g):
    assert not is_tree(Graph())

    for i in range(MAX):
        g.link(i, (i + 1) % MAX)

    assert not is_tree(g)


def test_cycle_true(g):
    for v1 in g.vertices:
        for v2 in g.vertices:
            if v1 != v2 and not g.has_edge(v1, v2):
                g.link(v1, v2, (v1 + v2) % 5)

    assert has_cycle(g)


def test_cycle_false(g):
    assert not has_cycle(Graph())

    vertices = list(g.vertices)

    for v1, v2 in zip(vertices, vertices[1:]):
        g.link(v1, v2, (v1 + v2) % 5)

    assert not has_cycle(g)


def test_transitive_closure(g):
    for i in range(MAX):
        assert transitive_closure(g, i) == {i}

    for i in range(0, MAX, 2):
        g.link(i, (i + 1) % MAX)

    for i in range(0, MAX, 2):
        assert transitive_closure(g, i) == {i, (i + 1) % MAX}

    for i in range(1, MAX, 2):
        assert transitive_closure(g, i) == {i - 1, i}

    for i in range(1, MAX, 2):
        g.link(i, (i + 1) % MAX)

    assert is_connected(g)

    for i in range(MAX):
        assert transitive_closure(g, i) == g.vertices
