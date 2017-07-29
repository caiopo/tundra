Tundra
======

[![Build Status](https://travis-ci.org/caiopo/tundra.svg?branch=master)](https://travis-ci.org/caiopo/graph) [![Coverage Status](https://coveralls.io/repos/github/caiopo/tundra/badge.svg?branch=master)](https://coveralls.io/github/caiopo/tundra?branch=master)

Pure Python, no dependencies Graph Algorithms module

Structures
----------
- [Graph class](tundra/core/graph.py)
- [Digraph class](tundra/core/digraph.py)

Algorithms
----------
### Search
- [Depth-first search](tundra/algorithm/search.py)
- [Breadth-first search](tundra/algorithm/search.py)

### Spanning tree
- [Kruskal's Algorithm](tundra/algorithm/spanning_tree.py)
- [Prim's Algorithm](tundra/algorithm/spanning_tree.py)

### Shortest path
- [Dijskra's Algoritm](tundra/algorithm/path.py)
- [Floyd-Warshall Algoritm](tundra/algorithm/path.py)

### Miscellaneous
- [Fringe](tundra/algorithm/misc.py)
- [Greedy coloring](tundra/algorithm/misc.py)
- [Proprety tests (is\_tree, is\_complete, ...)](tundra/algorithm/tests.py)

Utilities
---------
- [DOT language conversion](tundra/util.py)
- [Export Graph to PNG](tundra/util.py)
