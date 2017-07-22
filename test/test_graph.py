import pytest

from context import Graph

MAX_N = 100


@pytest.fixture
def g():
    return Graph(range(MAX_N))


def test_init():
    vertices = {1, 2, 3, 4}
    edges = {(1, 2), (2, 3, 10), (3, 4)}

    expected_edges = {(1, 2, 1), (2, 3, 10), (3, 4, 1)}

    g = Graph(set(vertices), set(edges))

    assert g.vertices == vertices
    assert g.edges == expected_edges


def test_add_vertex(g):
    for i in range(MAX_N):
        assert i in g.vertices


def test_add_raises(g):
    g = Graph()
    g.insert(0)

    with pytest.raises(KeyError):
        g.insert(0)


def test_remove_vertex(g):
    for i in range(MAX_N):
        g.remove(i)

    assert g.order == 0


def test_remove_raises(g):
    with pytest.raises(KeyError):
        Graph().remove(0)


def test_add_edge(g):
    for i in range(MAX_N):
        g.link(i, (i + 1) % MAX_N)

    for i in range(MAX_N):
        assert (i + 1) % MAX_N in g.neighbors(i)

        assert i in g.neighbors((i + 1) % MAX_N)


def test_add_edge_raises(g):
    with pytest.raises(KeyError):
        Graph().link(0, 1)


def test_remove_edge_commutative(g):
    for i in range(MAX_N):
        g.link(i, (i + 1) % MAX_N)

    for i in range(MAX_N):
        g.unlink((i + 1) % MAX_N, i)

    for i in range(MAX_N):
        assert i not in g.neighbors(i)


def test_remove_edge_neighbors(g):
    for v in range(1, MAX_N):
        g.link(0, v)

    assert g.edges == {(0, v, 1) for v in range(1, MAX_N)}

    g.remove(0)

    assert g.edges == set()


def test_remove_edge_raises(g):
    with pytest.raises(KeyError):
        Graph().unlink(0, 1)


def test_get_weight(g):
    for i in range(MAX_N):
        g.link(i, (i + 1) % MAX_N, i**3)
        assert g.weight[i, (i + 1) % MAX_N] == i**3


def test_set_weight(g):
    for i in range(MAX_N):
        g.link(i, (i + 1) % MAX_N, i**3)
        assert g.weight[i, (i + 1) % MAX_N] == i**3

    for i in range(MAX_N):
        g.weight[i, (i + 1) % MAX_N] = 2**i
        assert g.weight[i, (i + 1) % MAX_N] == 2**i


def test_set_weight_raises(g):
    g = Graph(range(5))

    with pytest.raises(KeyError):
        g.weight[1, 2] = 5

    with pytest.raises(KeyError):
        g.weight[42, 2] = 5


def test_order(g):
    gr = Graph()

    assert gr.order == 0

    for i in range(MAX_N):
        gr.insert(i)
        assert gr.order == i + 1


def test_vertices(g):
    vertices = g.vertices

    for i in range(MAX_N):
        assert i in vertices


def test_neighbors(g):
    for i in range(MAX_N):
        g.link(i, (2 * i) % MAX_N)
        g.link(i, (3 * i) % MAX_N)
        g.link(i, (4 * i) % MAX_N)

    for i in range(MAX_N):
        adj = g.neighbors(i)

        assert (2 * i) % MAX_N in adj
        assert (3 * i) % MAX_N in adj
        assert (4 * i) % MAX_N in adj


def test_degree(g):
    for i in range(MAX_N):
        assert g.degree(i) == 0

    for i in range(MAX_N):
        g.link(i, (i + 1) % MAX_N)

    for i in range(MAX_N):
        assert g.degree(i) == 2

    for i in range(MAX_N):
        g.link(i, (i + 2) % MAX_N)

    for i in range(MAX_N):
        assert g.degree(i) == 4


def test_regular(g):
    assert g.is_regular()

    g.link(0, 1)

    assert not g.is_regular()

    for i in range(1, MAX_N):
        g.link(i, (i + 1) % MAX_N)

    assert g.is_regular()

    g.link(1, 3)

    assert not g.is_regular()


def test_complete(g):
    assert not g.is_complete()

    for i in range(MAX_N):
        for j in range(MAX_N):
            g.link(i, j)

    assert not g.is_complete()

    for i in range(MAX_N):
        g.unlink(i, i)

    assert g.is_complete()


def test_connected(g):
    assert not g.is_connected()

    for i in range(0, MAX_N, 2):
        g.link(i, i + 1)

    assert not g.is_connected()

    for i in range(1, MAX_N, 2):
        g.link(i, (i + 1) % MAX_N)

    assert g.is_connected()


def test_tree_true(g):
    for i in range(MAX_N):
        if (2 * i + 1) < MAX_N:
            g.link(i, 2 * i + 1)

        if (2 * i + 2) < MAX_N:
            g.link(i, 2 * i + 2)

    assert g.is_tree()


def test_tree_false(g):
    for i in range(MAX_N):
        g.link(i, (i + 1) % MAX_N)

    assert not g.is_tree()


def test_cycle_true(g):
    for v1 in g.vertices:
        for v2 in g.vertices:
            if v1 != v2:
                g.link(v1, v2, (v1 + v2) % 5)

    assert g.has_cycle()


def test_cycle_false(g):
    vertices = list(g.vertices)

    for v1, v2 in zip(vertices, vertices[1:]):
        g.link(v1, v2, (v1 + v2) % 5)

    assert not g.has_cycle()


def test_transitive_closure(g):
    for i in range(MAX_N):
        assert g.transitive_closure(i) == {i}

    for i in range(0, MAX_N, 2):
        g.link(i, (i + 1) % MAX_N)

    for i in range(0, MAX_N, 2):
        assert g.transitive_closure(i) == {i, (i + 1) % MAX_N}

    for i in range(1, MAX_N, 2):
        assert g.transitive_closure(i) == {i - 1, i}

    for i in range(1, MAX_N, 2):
        g.link(i, (i + 1) % MAX_N)

    assert g.is_connected()

    for i in range(MAX_N):
        assert g.transitive_closure(i) == g.vertices


def test_str(g):
    g = Graph()

    assert str(g) == 'Graph(set(), set())'

    g.insert(0)
    g.insert(1)

    assert str(g) == 'Graph({0, 1}, set())'

    g.link(0, 1, 5)

    assert str(g) == 'Graph({0, 1}, {(0, 1, 5)})'
