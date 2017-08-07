Tundra
======

<!-- nopypi  -->
[![Build Status](https://travis-ci.org/caiopo/tundra.svg?branch=master)](https://travis-ci.org/caiopo/graph) [![Coverage Status](https://coveralls.io/repos/github/caiopo/tundra/badge.svg?branch=master)](https://coveralls.io/github/caiopo/tundra?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/9e2d5134e9244501b10fafe5a2e85556)](https://www.codacy.com/app/caiopo/tundra?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=caiopo/tundra&amp;utm_campaign=Badge_Grade) [![PyPI](https://img.shields.io/pypi/v/tundra.svg)](https://pypi.python.org/pypi/tundra) [![PyPI](https://img.shields.io/pypi/pyversions/tundra.svg)](https://pypi.python.org/pypi/tundra) [![PyPI](https://img.shields.io/pypi/l/tundra.svg)](https://pypi.python.org/pypi/tundra)
<!-- endnopypi  -->


Pure Python Graph Algorithms module

Installing
----------
`pip install tundra`


Overview
--------

### Structures
- [Graph class](tundra/core/graph.py)
- [Digraph class](tundra/core/digraph.py)

### Algorithms

#### Search
- [Depth-first search](tundra/algorithm/search.py)
- [Breadth-first search](tundra/algorithm/search.py)

#### Spanning tree
- [Kruskal's Algorithm](tundra/algorithm/spanning_tree.py)
- [Prim's Algorithm](tundra/algorithm/spanning_tree.py)

#### Path
- [Dijskra's Algoritm](tundra/algorithm/path.py)
- [Floyd-Warshall Algoritm](tundra/algorithm/path.py)
- [Nearest-neighbors hamiltonian cycle](tundra/algorithm/path.py)

#### Miscellaneous
- [Fringe](tundra/algorithm/misc.py)
- [Greedy coloring](tundra/algorithm/misc.py)
- [Proprety tests (is\_tree, is\_complete, ...)](tundra/algorithm/tests.py)

### Utilities
- [DOT language conversion](tundra/util.py)
- [Export Graph to PNG](tundra/util.py)
