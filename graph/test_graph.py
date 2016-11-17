import unittest

from graph import Graph, GraphException

MAX_N = 100

class GraphTest(unittest.TestCase):
    def setUp(self):
        self.g = Graph()

        for i in range(MAX_N):
            self.g.add_vertex(i)

    def test_add_vertex(self):
        for i in range(MAX_N):
            self.assertIn(i, self.g.vertices(),
                'i should be a vertex')

    def test_remove_vertex(self):
        for i in range(MAX_N):
            self.g.remove_vertex(i)

        self.assertEqual(self.g.order(), 0,
            'the graph should be empty')

    def test_remove_raises(self):
        with self.assertRaises(KeyError,
            msg='removing an inexistent vertex should raise an exception'):

            Graph().remove_vertex(0)

    def test_add_edge(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertIn((i + 1) % MAX_N, self.g.neighbors(i),
                'these vertices should be connected')

            self.assertIn(i, self.g.neighbors((i + 1) % MAX_N),
                'these vertices should be connected')

    def test_add_edge_raises(self):
        with self.assertRaises(KeyError,
            msg='connecting inexistent vertices should raise an exception'):
            Graph().add_edge(0, 1)

    def test_remove_edge(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.g.remove_edge((i + 1) % MAX_N, i)

        for i in range(MAX_N):
            self.assertNotIn(i, self.g.neighbors(i),
                'these vertices should not be connected')

    def test_remove_edge_raises(self):
        with self.assertRaises(KeyError,
            msg='disconnecting inexistent vertices should raise an exception'):
            Graph().remove_edge(0, 1)

    def test_order(self):
        gr = Graph()

        self.assertEqual(gr.order(), 0,
            'order should be 0 (graph with no vertices)')

        for i in range(MAX_N):
            gr.add_vertex(i)
            self.assertEqual(gr.order(), i+1,
                'order deveria ser igual ao número de vértices no grafo')

    def test_vertices(self):
        vertices = self.g.vertices()

        for i in range(MAX_N):
            self.assertIn(i, vertices,
                '{} should be a vertex of the graph'.format(i))

    def test_rand_vertex(self):
        gr = Graph()

        gr.add_vertex(0)

        self.assertEqual(gr.rand_vertex(), 0)

        gr.remove_vertex(0)

        gr.add_vertex(1)

        self.assertEqual(gr.rand_vertex(), 1)

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

    def test_completo(self):
        self.assertFalse(self.g.is_complete())

        for i in range(MAX_N):
            for j in range(MAX_N):
                self.g.add_edge(i, j)

        self.assertFalse(self.g.is_complete())

        for i in range(MAX_N):
            self.g.remove_edge(i, i)

        self.assertTrue(self.g.is_complete())

    def test_conexo(self):
        self.assertFalse(self.g.is_connected(),
            'should not be connected')

        for i in range(0, MAX_N, 2):
            self.g.add_edge(i, i+1)

        self.assertFalse(self.g.is_connected(),
            'should not be connected')

        for i in range(1, MAX_N, 2):
            self.g.add_edge(i, (i + 1) % MAX_N)

        self.assertTrue(self.g.is_connected(),
            'should be connected')

    def test_arvore_true(self):
        for i in range(MAX_N):
            if (2 * i + 1) < MAX_N:
                self.g.add_edge(i, 2 * i + 1)

            if (2 * i + 2) < MAX_N:
                self.g.add_edge(i, 2 * i + 2)

        self.assertTrue(self.g.is_tree(), 'should be a tree')

    def test_arvore_false(self):
        for i in range(MAX_N):
            self.g.add_edge(i, (i + 1) % MAX_N)

        self.assertFalse(self.g.is_tree(), 'should not be a tree')

    def test_transitive_closure(self):
        for i in range(MAX_N):
            self.assertEqual(self.g.transitive_closure(i), {i})

        for i in range(0, MAX_N, 2):
            self.g.add_edge(i, (i + 1) % MAX_N)

        for i in range(0, MAX_N, 2):
            self.assertEqual(self.g.transitive_closure(i), {i, (i + 1) % MAX_N})

        for i in range(1, MAX_N, 2):
            self.assertEqual(self.g.transitive_closure(i), {i - 1, i})

        for i in range(1, MAX_N, 2):
            self.g.add_edge(i, (i + 1) % MAX_N)

        self.assertTrue(self.g.is_connected())

        for i in range(MAX_N):
            self.assertEqual(self.g.transitive_closure(i), self.g.vertices())

if __name__ == '__main__':
    unittest.main()
