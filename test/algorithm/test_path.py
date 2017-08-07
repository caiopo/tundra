import pytest

from context import (Graph, dijkstra, floyd_warshall, hamiltonian_cycle,
                     shortest_distance, HamiltonianCycleNotFound)


@pytest.fixture
def g1():
    return Graph(
        range(1, 5),
        {
            (1, 2, 24),
            (1, 4, 20),
            (3, 1, 3),
            (4, 3, 12),
        }
    )


@pytest.fixture
def g2():
    return Graph(
        range(9),
        {
            (5, 6, 2), (1, 2, 8), (6, 8, 6), (1, 7, 11), (2, 5, 4), (7, 8, 7),
            (0, 7, 8), (6, 7, 1), (3, 5, 14), (2, 3, 7), (3, 4, 9), (2, 8, 2),
            (0, 1, 4), (4, 5, 10),
        }
    )


def test_shortest_distance(g1, g2):
    assert shortest_distance(g1, 1) == {1: 0, 2: 24, 3: 3, 4: 15}

    assert shortest_distance(g2, 0) == {
        0: 0,
        1: 4,
        2: 12,
        3: 19,
        4: 21,
        5: 11,
        6: 9,
        7: 8,
        8: 14,
    }


def test_dijkstra(g2):
    assert dijkstra(g2, 0, 4) == [0, 7, 6, 5, 4]

    assert dijkstra(g2, 4, 0) == [4, 5, 6, 7, 0]

    assert dijkstra(g2, 3, 0) == [3, 2, 1, 0]


@pytest.mark.parametrize('graph', [g1(), g2()])
def test_floyd_warshall(graph):
    fw = floyd_warshall(graph)

    for v in graph.vertices:
        assert fw[v] == shortest_distance(graph, v)


def test_hamiltonian_cycle():
    g = Graph(
        range(11),
        zip(range(10), range(1, 10)),
    )

    for v in range(10):

        g.link(v, 10, 2)

    hc = hamiltonian_cycle(g, 0)

    assert hc == list(range(11))


def test_hamiltonian_cycle_raises():
    g = Graph(
        range(3),
        ((0, 1), (1, 2)),
    )

    with pytest.raises(HamiltonianCycleNotFound):
        hamiltonian_cycle(g, 1)
