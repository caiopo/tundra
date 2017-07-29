from itertools import product

import pytest

from context import (Graph, biclique, binary_tree, complete, crown, is_tree,
                     lattice)

lattice_test1 = Graph(
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
        14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24},
    {
        (0, 1), (2, 7), (17, 18), (5, 6), (4, 9), (6, 7), (8, 9), (10, 15),
        (3, 4), (7, 8), (15, 16), (15, 20), (13, 14), (21, 22), (2, 3), (0, 5),
        (17, 22), (8, 13), (10, 11), (22, 23), (3, 8), (11, 12), (23, 24),
        (6, 11), (14, 19), (12, 17), (1, 2), (16, 17), (18, 23), (5, 10),
        (19, 24), (12, 13), (20, 21), (1, 6), (16, 21), (18, 19), (11, 16),
        (9, 14), (7, 12), (13, 18)
    }
)

lattice_test2 = Graph(
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},
    {
        (11, 13), (0, 1), (1, 3), (6, 7), (8, 9), (0, 2),
        (2, 4), (9, 11), (2, 3), (14, 15), (8, 10),
        (10, 12), (10, 11), (4, 5), (16, 17), (5, 7),
        (17, 19), (4, 6), (6, 8), (14, 16), (12, 13),
        (16, 18), (18, 19), (3, 5), (7, 9), (15, 17),
        (13, 15), (12, 14)
    }
)

lattice_test3 = Graph(
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
    {
        (0, 1), (2, 7), (5, 6), (4, 9), (6, 7), (8, 9),
        (3, 4), (7, 8), (13, 14), (2, 3), (0, 5), (8, 13),
        (10, 11), (3, 8), (11, 12), (6, 11), (1, 2), (5, 10),
        (12, 13), (1, 6), (9, 14), (7, 12)
    }
)

lattice_test4 = Graph(
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
    {
        (1, 2), (0, 1), (2, 7), (4, 9), (2, 3), (6, 7),
        (3, 8), (0, 5), (8, 9), (3, 4), (7, 8), (5, 6),
        (1, 6)
    }
)


def test_complete():
    for size in range(20):
        g = complete(size)

        for v1, v2 in product(g.vertices, g.vertices):
            assert g.has_edge(v1, v2) == (v1 is not v2)


def test_biclique():
    sizes = list(range(21))

    for s1, s2 in product(sizes, sizes):
        vertices1 = set(range(s1))
        vertices2 = set(range(s1, s1 + s2 + 1))

        g = biclique(vertices1, vertices2)

        for v1 in vertices1:
            assert g.neighbors(v1) == vertices2

        for v2 in vertices2:
            assert g.neighbors(v2) == vertices1


def test_crown():
    for size in range(1, 21):
        vertices1 = list(range(size))
        vertices2 = list(range(size, 2 * size))

        g = crown(vertices1, vertices2)

        for i, v1 in enumerate(vertices1):
            neigh2 = set(vertices2) - {vertices2[i]}

            assert g.neighbors(v1) == neigh2

        for i, v2 in enumerate(vertices2):
            neigh1 = set(vertices1) - {vertices1[i]}

            assert g.neighbors(v2) == neigh1


def test_crown_raises():
    with pytest.raises(ValueError):
        crown(1, 2)

    with pytest.raises(ValueError):
        crown(1000, 6)

    with pytest.raises(ValueError):
        crown(300, 301)

    with pytest.raises(ValueError):
        crown(-1, 2)

    with pytest.raises(ValueError):
        crown(10, -1)

    with pytest.raises(ValueError):
        crown(-42, -1)


def test_lattice():
    g1 = lattice(25)
    assert g1 == lattice_test1

    g2 = lattice(20, height=10)
    assert g2 == lattice_test2

    g3 = lattice(15, width=5)
    assert g3 == lattice_test3

    g4 = lattice(10, width=5, height=2)
    assert g4 == lattice_test4


def test_lattice_raises():
    with pytest.raises(ValueError):
        lattice(3)

    with pytest.raises(ValueError):
        lattice(range(3))

    with pytest.raises(ValueError):
        lattice(10, width=6)

    with pytest.raises(ValueError):
        lattice(10, height=6)

    with pytest.raises(ValueError):
        lattice(width=0, height=10)

    with pytest.raises(ValueError):
        lattice(width=10, height=0)

    with pytest.raises(ValueError):
        lattice(-42)

    with pytest.raises(ValueError):
        lattice(width=0, height=0)

    with pytest.raises(ValueError):
        lattice(width=10)

    with pytest.raises(ValueError):
        lattice(20, width=0)

    with pytest.raises(ValueError):
        lattice(20, height=0)

    with pytest.raises(ValueError):
        lattice(20, width=3, height=10,)


def test_binary_tree():
    with pytest.raises(ValueError):
        binary_tree(0)

    for i in range(1, 20):
        g = binary_tree(i)

        assert is_tree(g)
