import unittest

from context import Graph, fringe


class TestUtil(unittest.TestCase):
    def test_fringe(self):
        g = Graph(range(10))

        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(0, 3)
        g.add_edge(0, 4)

        g.add_edge(1, 5)
        g.add_edge(1, 6)
        g.add_edge(1, 7)
        g.add_edge(1, 8)

        g.add_edge(2, 9)

        self.assertEqual(fringe(g, [0]), set(range(1, 5)))

        self.assertEqual(fringe(g, [1]), {0} | set(range(5, 9)))

        self.assertEqual(fringe(g, [2]), {0, 9})

        self.assertEqual(fringe(g, [0, 1]), set(range(2, 9)))

        self.assertEqual(fringe(g, [0, 1, 2]), g.vertices - {0, 1, 2})

    def test_fringe_raises(self):
        g = Graph()

        with self.assertRaises(ValueError):
            fringe(g, [0])
