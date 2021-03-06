"""
This file solves the following problem:

"Once upon a time a farmer went to a market and purchased a wolf, a sheep, and
a cabbage. On his way home, the farmer came to the bank of a river and
rented a boat. But in crossing the river by boat, the farmer could carry only
himself and a single one of his purchases: the wolf, the sheep, or the
cabbage.

If left unattended together, the wolf would eat the sheep, or the sheep would
eat the cabbage.

The farmer's challenge was to carry himself and his purchases to the far bank
of the river, leaving each purchase intact. How did he do it?"

Text adapted from Wikipedia

Usage:

python ./wolf_sheep_cabbage.py [graph.png]
"""

from itertools import product
from sys import argv
from typing import NamedTuple

from tundra import Graph, algorithm, util


class State(NamedTuple):
    """
    Represents the presence of the wolf, the sheep, the cabbage and
    the boat (with the farmer) on the starting side
    """
    wolf: bool
    sheep: bool
    cabbage: bool
    boat: bool

    def __str__(self):
        return (f'({int(self.wolf)},'
                f' {int(self.sheep)},'
                f' {int(self.cabbage)},'
                f' {int(self.boat)})')

    def __repr__(self):
        return str(self)


def valid(state):
    w, s, c, b = state

    return (w != s or w == b) and (s != c or s == b)


def has_edge(s1, s2):
    if s1.boat == s2.boat:
        return False

    w = s1.wolf == s2.wolf
    s = s1.sheep == s2.sheep
    c = s1.cabbage == s2.cabbage

    return (w + s + c) in (2, 3)


def export_solution(graph, solution):
    if len(argv) > 1:
        solution_edges = set(zip(solution, solution[1:]))

        util.export_png(
            graph,
            argv[1],
            command=util.Filter.DOT,
            edge_color=(
                lambda v1, v2, w: 'red' if (
                    (v1, v2) in solution_edges or
                    (v2, v1) in solution_edges
                ) else None
            )
        )


states = {
    s
    for s in (State(*t) for t in product({True, False}, repeat=4))
    if valid(s)
}

graph = Graph(
    states,
    {
        (min(s1, s2), max(s1, s2))
        for s1, s2 in product(states, repeat=2)
        if has_edge(s1, s2)
    }
)


initial = State(True, True, True, True)

final = State(False, False, False, False)

solution = algorithm.dijkstra(graph, initial, final)

export_solution(graph, solution)

print(*solution, sep='\n')

print('The solution took', len(solution), 'steps.')
