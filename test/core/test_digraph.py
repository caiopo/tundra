import pytest

from context import Digraph
from itertools import repeat


@pytest.fixture
def dg():
    return Digraph(range(10))


def knot(dg):
    vl = list(dg.vertices)

    edges = [
        (v, (i + 1) % len(vl))
        for i, v in enumerate(vl)
    ]

    for t in edges:
        dg.link(*t)

    return edges


def test_init():
    dg = Digraph(
        range(10),
        zip(range(10), range(1, 10))
    )

    assert dg.vertices == set(range(10))

    assert dg.edges == set(zip(range(10), range(1, 10), repeat(1)))


def test_remove(dg):
    knot(dg)

    for v in dg.vertices:
        dg.remove(v)

    assert dg.vertices == set()
    assert dg.edges == set()


def test_link_raises(dg):
    dg.link(0, 1)

    with pytest.raises(ValueError):
        dg.link(0, 1)


def test_unlink(dg):
    for v in dg.vertices:
        for w in dg.vertices - {v}:
            dg.link(v, w)

    for v in dg.vertices:
        for w in dg.vertices - {v}:
            dg.unlink(v, w)

    assert dg.edges == set()


def test_unlink_raises(dg):
    with pytest.raises(ValueError):
        dg.unlink(0, 1)


def test_predecessors(dg):
    for v in dg.vertices:
        assert dg.predecessors(v) == set()
        assert dg.indegree(v) == 0

    for v, w in knot(dg):
        assert dg.predecessors(w) == {v}

        assert dg.indegree(w) == 1


def test_successors(dg):
    for v in dg.vertices:
        assert dg.successors(v) == set()

        assert dg.outdegree(v) == 0

    for v, w in knot(dg):
        assert dg.successors(v) == {w}

        assert dg.outdegree(v) == 1


def test_neighbors(dg):
    for v in dg.vertices:
        assert dg.neighbors(v) == set()
        assert dg.degree(v) == 0
