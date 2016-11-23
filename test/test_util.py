import unittest

from context import Graph, util

class TestUtil(unittest.TestCase):
    def test_fringe(self):
        g = Graph(range(10))

        print(g)


if __name__ == '__main__':
    unittest.main()
