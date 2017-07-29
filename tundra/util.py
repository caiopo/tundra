from os import remove
from subprocess import PIPE, run
from typing import Callable, Dict, Tuple

from tundra import Graph, Vertex
from tundra.algorithm import is_tree, is_complete

__all__ = ('Filter', 'to_dot', 'export_dot', 'export_png')


class Filter:
    DOT = 'dot'
    NEATO = 'neato'
    TWOPI = 'twopi'
    CIRCO = 'circo'
    FDP = 'fdp'
    SFDP = 'sfdp'
    PATCHWORK = 'patchwork'


VertexToString = Callable[[Vertex], str]
EdgeToColor = Callable[[Vertex, Vertex, int], str]


def to_dot(g: Graph,
           name: str = None,
           to_str: VertexToString = str,
           force_weight: bool = False,
           edge_color: EdgeToColor = None) -> str:

    name = name or str(hash(str(g)))
    edge_color = edge_color or (lambda *args: None)

    dot = ['graph {\n']

    for v1, v2, w in g.edges:
        dot += ['"', to_str(v1), '" -- "', to_str(v2), '"']

        color = edge_color(v1, v2, w)

        if w != 1 or force_weight:
            dot += [
                ' [',
                f'label="{str(w)}"',
                f'color="{color}"' if color is not None else '',
                ']']

        dot.append(';\n')

    for v in g.vertices:
        if len(g.neighbors(v)) == 0:
            dot += ['"', to_str(v), '";\n']

    dot.append('}')

    return ''.join(dot)


def export_dot(g: Graph, filename: str, **kwargs):
    dot = to_dot(g, **kwargs)

    with open(filename, 'w') as file:
        file.write(dot)


def export_png(g: Graph, filename: str, command: str = None, **kwargs):
    dot = to_dot(g, **kwargs)

    if not command:
        if is_tree(g):
            command = Filter.DOT
        elif is_complete(g):
            command = Filter.CIRCO
        else:
            command = Filter.SFDP

    proc = run([command, '-Tpng'], input=dot.encode('utf-8'),
               stdout=PIPE, check=True)

    with open(filename, 'wb') as file:
        file.write(proc.stdout)
