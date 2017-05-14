import unittest

from context import Graph, prim


class UtilTest(unittest.TestCase):
    def test_prim(self):
        g = Graph(range(10))

        for v in g.vertices:
            g.add_edge(0, v, 5)

        for v1 in g.vertices:
            for v2 in g.vertices:
                if v1 != v2 and not g.has_edge(v1, v2):
                    g.add_edge(v1, v2, 10)

        tree = prim(g)

        self.assertEqual(tree.vertices, set(range(10)))

        self.assertEqual(tree.edges, {(0, i, 5) for i in range(1, 10)})
