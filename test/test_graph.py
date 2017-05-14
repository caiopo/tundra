import unittest

from context import Graph

MAX_N = 100


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.g = Graph(range(MAX_N))

    def test_init(self):
        vertices = {1, 2, 3, 4}
        edges = {(1, 2), (2, 3, 10), (3, 4)}

        expected_edges = {(1, 2, 1), (2, 3, 10), (3, 4, 1)}

        g = Graph(set(vertices), set(edges))

        self.assertEqual(g.vertices, vertices)
        self.assertEqual(g.edges, expected_edges)

    def test_add_vertex(self):
        for i in range(MAX_N):
            self.assertIn(i, self.g.vertices)

    def test_add_raises(self):
        g = Graph()
        g.add_vertex(0)

        with self.assertRaises(KeyError):
            g.add_vertex(0)

    def test_remove_vertex(self):
        for i in range(MAX_N):
            self.g.remove_vertex(i)

        self.assertEqual(self.g.order, 0)

    def test_remove_raises(self):
        with self.assertRaises(KeyError):
            Graph().remove_vertex(0)

    def test_add_edge(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertIn((i + 1) % MAX_N, self.g.neighbors(i))

            self.assertIn(i, self.g.neighbors((i + 1) % MAX_N))

    def test_add_edge_raises(self):
        with self.assertRaises(KeyError):
            Graph().add_edge(0, 1)

    def test_remove_edge_commutative(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.g.remove_edge((i + 1) % MAX_N, i)

        for i in range(MAX_N):
            self.assertNotIn(i, self.g.neighbors(i))

    def test_remove_edge_neighbors(self):
        for v in range(1, MAX_N):
            self.g.add_edge(0, v)

        self.assertEqual(self.g.edges, {(0, v, 1) for v in range(1, MAX_N)})

        self.g.remove_vertex(0)

        self.assertEqual(self.g.edges, set())

    def test_remove_edge_raises(self):
        with self.assertRaises(KeyError):
            Graph().remove_edge(0, 1)

    def test_get_weight(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N, i**3)
            self.assertEqual(self.g.get_weight(i, (i + 1) % MAX_N), i**3)

    def test_set_weight(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N, i**3)
            self.assertEqual(self.g.get_weight(i, (i + 1) % MAX_N), i**3)

        for i in range(MAX_N):
            self.g.set_weight(i, (i + 1) % MAX_N, 2**i)
            self.assertEqual(self.g.get_weight(i, (i + 1) % MAX_N), 2**i)

    def test_order(self):
        gr = Graph()

        self.assertEqual(gr.order, 0)

        for i in range(MAX_N):
            gr.add_vertex(i)
            self.assertEqual(gr.order, i + 1)

    def test_vertices(self):
        vertices = self.g.vertices

        for i in range(MAX_N):
            self.assertIn(i, vertices)

    def test_random_vertex(self):
        gr = Graph()

        gr.add_vertex(0)

        self.assertEqual(gr.random_vertex(), 0)

        gr.add_vertex(1)

        gr.remove_vertex(0)

        self.assertEqual(gr.random_vertex(), 1)

    def test_neighbors(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (2 * i) % MAX_N)
            self.g.add_edge(i, (3 * i) % MAX_N)
            self.g.add_edge(i, (4 * i) % MAX_N)

        for i in range(MAX_N):
            adj = self.g.neighbors(i)

            self.assertIn((2 * i) % MAX_N, adj)
            self.assertIn((3 * i) % MAX_N, adj)
            self.assertIn((4 * i) % MAX_N, adj)

    def test_degree(self):
        for i in range(MAX_N):
            self.assertEqual(self.g.degree(i), 0)

        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertEqual(self.g.degree(i), 2)

        for i in range(MAX_N):
            self.g.add_edge(i, (i + 2) % MAX_N)

        for i in range(MAX_N):
            self.assertEqual(self.g.degree(i), 4)

    def test_regular(self):
        self.assertTrue(self.g.is_regular())

        self.g.add_edge(0, 1)

        self.assertFalse(self.g.is_regular())

        for i in range(1, MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N)

        self.assertTrue(self.g.is_regular())

        self.g.add_edge(1, 3)

        self.assertFalse(self.g.is_regular())

    def test_complete(self):
        self.assertFalse(self.g.is_complete())

        for i in range(MAX_N):
            for j in range(MAX_N):
                self.g.add_edge(i, j)

        self.assertFalse(self.g.is_complete())

        for i in range(MAX_N):
            self.g.remove_edge(i, i)

        self.assertTrue(self.g.is_complete())

    def test_connected(self):
        self.assertFalse(self.g.is_connected())

        for i in range(0, MAX_N, 2):
            self.g.add_edge(i, i + 1)

        self.assertFalse(self.g.is_connected())

        for i in range(1, MAX_N, 2):
            self.g.add_edge(i, (i + 1) % MAX_N)

        self.assertTrue(self.g.is_connected())

    def test_tree_true(self):
        for i in range(MAX_N):
            if (2 * i + 1) < MAX_N:
                self.g.add_edge(i, 2 * i + 1)

            if (2 * i + 2) < MAX_N:
                self.g.add_edge(i, 2 * i + 2)

        self.assertTrue(self.g.is_tree())

    def test_tree_false(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N)

        self.assertFalse(self.g.is_tree())

    def test_transitive_closure(self):
        for i in range(MAX_N):
            self.assertEqual(self.g.transitive_closure(i), {i})

        for i in range(0, MAX_N, 2):
            self.g.add_edge(i, (i + 1) % MAX_N)

        for i in range(0, MAX_N, 2):
            self.assertEqual(self.g.transitive_closure(i),
                             {i, (i + 1) % MAX_N})

        for i in range(1, MAX_N, 2):
            self.assertEqual(self.g.transitive_closure(i), {i - 1, i})

        for i in range(1, MAX_N, 2):
            self.g.add_edge(i, (i + 1) % MAX_N)

        self.assertTrue(self.g.is_connected())

        for i in range(MAX_N):
            self.assertEqual(self.g.transitive_closure(i), self.g.vertices)

    def test_str(self):
        g = Graph()

        self.assertEqual(str(g), 'Graph(set(), set())')

        g.add_vertex(0)
        g.add_vertex(1)

        self.assertEqual(str(g), 'Graph({0, 1}, set())')

        g.add_edge(0, 1, 5)

        self.assertEqual(str(g), 'Graph({0, 1}, {(0, 1, 5)})')

