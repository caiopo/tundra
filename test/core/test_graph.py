import pytest

from context import Graph

MAX = 100


@pytest.fixture
def g():
    return Graph(range(MAX))


def test_init():
    vertices = {1, 2, 3, 4}
    edges = {(1, 2), (2, 3, 10), (3, 4)}

    expected_edges = {(1, 2, 1), (2, 3, 10), (3, 4, 1)}

    g = Graph(set(vertices), set(edges))

    assert g.vertices == vertices
    assert g.edges == expected_edges


def test_add_vertex(g):
    for i in range(MAX):
        assert i in g.vertices


def test_add_raises(g):
    g = Graph()
    g.insert(0)

    with pytest.raises(KeyError):
        g.insert(0)


def test_remove_vertex(g):
    for i in range(MAX):
        g.remove(i)

    assert g.order == 0


def test_remove_raises(g):
    with pytest.raises(KeyError):
        Graph().remove(0)


def test_add_edge(g):
    for i in range(MAX):
        g.link(i, (i + 1) % MAX)

    for i in range(MAX):
        assert (i + 1) % MAX in g.neighbors(i)

        assert i in g.neighbors((i + 1) % MAX)


def test_add_edge_raises(g):
    with pytest.raises(KeyError):
        Graph().link(0, 1)


def test_remove_edge_commutative(g):
    for i in range(MAX):
        g.link(i, (i + 1) % MAX)

    for i in range(MAX):
        g.unlink((i + 1) % MAX, i)

    for i in range(MAX):
        assert i not in g.neighbors(i)


def test_remove_edge_neighbors(g):
    for v in range(1, MAX):
        g.link(0, v)

    assert g.edges == {(0, v, 1) for v in range(1, MAX)}

    g.remove(0)

    assert g.edges == set()


def test_remove_edge_raises(g):
    with pytest.raises(KeyError):
        Graph().unlink(0, 1)


def test_get_weight(g):
    for i in range(MAX):
        g.link(i, (i + 1) % MAX, i**3)
        assert g.weight[i, (i + 1) % MAX] == i**3


def test_set_weight(g):
    for i in range(MAX):
        g.link(i, (i + 1) % MAX, i**3)
        assert g.weight[i, (i + 1) % MAX] == i**3

    for i in range(MAX):
        g.weight[i, (i + 1) % MAX] = 2**i
        assert g.weight[i, (i + 1) % MAX] == 2**i


def test_set_weight_raises(g):
    g = Graph(range(5))

    with pytest.raises(KeyError):
        g.weight[1, 2] = 5

    with pytest.raises(KeyError):
        g.weight[42, 2] = 5


def test_order(g):
    gr = Graph()

    assert gr.order == 0

    for i in range(MAX):
        gr.insert(i)
        assert gr.order == i + 1


def test_vertices(g):
    vertices = g.vertices

    for i in range(MAX):
        assert i in vertices


def test_neighbors(g):
    for i in range(MAX):
        vs = {
            (2 * i) % MAX,
            (3 * i) % MAX,
            (4 * i) % MAX,
        }

        for v in vs:
            if not g.has_edge(i, v):
                g.link(i, v)

    for i in range(MAX):
        adj = g.neighbors(i)

        assert (2 * i) % MAX in adj
        assert (3 * i) % MAX in adj
        assert (4 * i) % MAX in adj


def test_degree(g):
    for i in range(MAX):
        assert g.degree(i) == 0

    for i in range(MAX):
        g.link(i, (i + 1) % MAX)

    for i in range(MAX):
        assert g.degree(i) == 2

    for i in range(MAX):
        g.link(i, (i + 2) % MAX)

    for i in range(MAX):
        assert g.degree(i) == 4


def test_str(g):
    g = Graph()

    assert str(g) == 'Graph(set(), set())'

    g.insert(0)
    g.insert(1)

    assert str(g) == 'Graph({0, 1}, set())'

    g.link(0, 1, 5)

    assert str(g) == 'Graph({0, 1}, {(0, 1, 5)})'
