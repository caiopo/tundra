from subprocess import run
from typing import Callable

from tundra import Graph, Vertex
from tundra.algorithm import is_complete, is_tree

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


def to_dot(
    g: Graph,
    to_str: VertexToString = str,
    force_weight: bool = False,
    edge_color: EdgeToColor = None
) -> str:
    edge_color = edge_color or (lambda *args: None)

    dot = ['graph {\n']

    for v1, v2, w in g.edges:
        dot += ['"', to_str(v1), '" -- "', to_str(v2), '"']

        opts = []

        if w != 1 or force_weight:
            opts.append(f'label="{str(w)}"')

        color = edge_color(v1, v2, w)

        if color is not None:
            opts.append(f'color="{color}"')

        if len(opts) > 0:
            dot += [
                ' [',
                *opts,
                ']'
            ]

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

    with open(filename, 'wb') as file:
        run(
            [command, '-Tpng'],
            input=dot.encode('utf-8'),
            stdout=file,
            check=True,
        )
