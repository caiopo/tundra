import pytest

from context import Graph, dijkstra, floyd_warshall, shortest_distance


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
            (0, 1, 4), (0, 7, 8), (1, 0, 4), (1, 2, 8), (1, 7, 11),
            (2, 1, 8), (2, 3, 7), (2, 5, 4), (2, 8, 2), (3, 2, 7),
            (3, 4, 9), (3, 5, 14), (4, 3, 9), (4, 5, 10), (5, 2, 4),
            (5, 3, 14), (5, 4, 10), (5, 6, 2), (6, 5, 2), (6, 7, 1),
            (6, 8, 6), (7, 0, 8), (7, 1, 11), (7, 6, 1), (7, 8, 7),
            (8, 2, 2), (8, 6, 6), (8, 7, 7)
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
    print('oi mãe')
    fw = floyd_warshall(graph)

    for v in graph.vertices:
        assert fw[v] == shortest_distance(graph, v)
