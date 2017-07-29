from context import Graph, bfs, dfs


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
