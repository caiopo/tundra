import pytest

from context import Graph, coloring, complete, fringe


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


def test_coloring_complete():
    for i in range(21):
        g = complete(i)

        n_colors = len({c for _, c in coloring(g).items()})

        assert n_colors == i


def test_coloring_sparse():
    assert len(coloring(Graph())) == 0

    for i in range(1, 21):
        g = Graph(range(i))

        n_colors = len({c for _, c in coloring(g).items()})

        assert n_colors == 1
