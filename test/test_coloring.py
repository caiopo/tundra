import unittest

from context import Graph, coloring, complete


class TestColoring(unittest.TestCase):
    def test_coloring_complete(self):
        for i in range(21):
            g = complete(i)

            n_colors = len({c for _, c in coloring(g).items()})

            self.assertEqual(n_colors, i)

    def test_coloring_sparse(self):
        self.assertEqual(len(coloring(Graph())), 0)

        for i in range(1, 21):
            g = Graph(range(i))

            n_colors = len({c for _, c in coloring(g).items()})

            self.assertEqual(n_colors, 1)
