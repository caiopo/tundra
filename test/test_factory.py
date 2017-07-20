import unittest
from itertools import product

from context import Graph, biclique, complete, crown, lattice


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
        (11, 13, 1), (0, 1, 1), (1, 3, 1), (6, 7, 1), (8, 9, 1), (0, 2, 1),
        (2, 4, 1), (9, 11, 1), (2, 3, 1), (14, 15, 1), (8, 10, 1),
        (10, 12, 1), (10, 11, 1), (4, 5, 1), (16, 17, 1), (5, 7, 1),
        (17, 19, 1), (4, 6, 1), (6, 8, 1), (14, 16, 1), (12, 13, 1),
        (16, 18, 1), (18, 19, 1), (3, 5, 1), (7, 9, 1), (15, 17, 1),
        (13, 15, 1), (12, 14, 1)
    }
)

lattice_test3 = Graph(
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
    {
        (0, 1, 1), (2, 7, 1), (5, 6, 1), (4, 9, 1), (6, 7, 1), (8, 9, 1),
        (3, 4, 1), (7, 8, 1), (13, 14, 1), (2, 3, 1), (0, 5, 1), (8, 13, 1),
        (10, 11, 1), (3, 8, 1), (11, 12, 1), (6, 11, 1), (1, 2, 1), (5, 10, 1),
        (12, 13, 1), (1, 6, 1), (9, 14, 1), (7, 12, 1)
    }
)

lattice_test4 = Graph(
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
    {
        (1, 2, 1), (0, 1, 1), (2, 7, 1), (4, 9, 1), (2, 3, 1), (6, 7, 1),
        (3, 8, 1), (0, 5, 1), (8, 9, 1), (3, 4, 1), (7, 8, 1), (5, 6, 1),
        (1, 6, 1)
    }
)


class TestColoring(unittest.TestCase):
    def test_complete(self):
        for size in range(20):
            g = complete(size)

            for v1, v2 in product(g.vertices, g.vertices):
                self.assertEqual(g.has_edge(v1, v2), v1 is not v2)

    def test_biclique(self):
        sizes = list(range(21))

        for s1, s2 in product(sizes, sizes):
            vertices1 = set(range(s1))
            vertices2 = set(range(s1, s1 + s2 + 1))

            g = biclique(vertices1, vertices2)

            for v1 in vertices1:
                self.assertEqual(g.neighbors(v1), vertices2)

            for v2 in vertices2:
                self.assertEqual(g.neighbors(v2), vertices1)

    def test_crown(self):
        sizes = list(range(21))

        for size in range(1, 21):
            vertices1 = list(range(size))
            vertices2 = list(range(size, 2 * size))

            g = crown(vertices1, vertices2)

            for i, v1 in enumerate(vertices1):
                neigh2 = set(vertices2) - {vertices2[i]}

                self.assertEqual(g.neighbors(v1), neigh2)

            for i, v2 in enumerate(vertices2):
                neigh1 = set(vertices1) - {vertices1[i]}

                self.assertEqual(g.neighbors(v2), neigh1)

    def test_crown_raises(self):
        with self.assertRaises(ValueError):
            crown(1, 2)

        with self.assertRaises(ValueError):
            crown(1000, 6)

        with self.assertRaises(ValueError):
            crown(300, 301)

        with self.assertRaises(ValueError):
            crown(-1, 2)

        with self.assertRaises(ValueError):
            crown(10, -1)

        with self.assertRaises(ValueError):
            crown(-42, -1)

    def test_lattice(self):
        g1 = lattice(25)

        self.assertEqual(g1, lattice_test1)

        g2 = lattice(20, height=10)
        self.assertEqual(g2, lattice_test2)

        g3 = lattice(15, width=5)
        self.assertEqual(g3, lattice_test3)

        g4 = lattice(10, width=5, height=2)
        self.assertEqual(g4, lattice_test4)

    def test_lattice_raises(self):
        with self.assertRaises(ValueError):
            lattice(3)

        with self.assertRaises(ValueError):
            lattice(range(3))

        with self.assertRaises(ValueError):
            lattice(10, width=6)

        with self.assertRaises(ValueError):
            lattice(10, height=6)

        with self.assertRaises(ValueError):
            lattice(width=0, height=10)

        with self.assertRaises(ValueError):
            lattice(width=10, height=0)

        with self.assertRaises(ValueError):
            lattice(-42)

        with self.assertRaises(ValueError):
            lattice(width=0, height=0)

        with self.assertRaises(ValueError):
            lattice(width=10)

        with self.assertRaises(ValueError):
            lattice(20, width=0)

        with self.assertRaises(ValueError):
            lattice(20, height=0)

        with self.assertRaises(ValueError):
            lattice(20, width=3, height=10,)