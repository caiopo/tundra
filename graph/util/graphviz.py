# from enum import Enum
from os import remove
from subprocess import run, PIPE
from tempfile import mkstemp
from typing import Callable

from graph import Graph, Vertex


# class Filter(Enum):
class Filter:
    DOT = 'dot'
    NEATO = 'neato'
    TWOPI = 'twopi'
    CIRCO = 'circo'
    FDP = 'fdp'
    SFDP = 'sfdp'
    PATCHWORK = 'patchwork'


VertexToString = Callable[[Vertex], str]


def to_dot(g: Graph, name: str = None, to_str: VertexToString = str,
           force_weight: bool = False) -> str:

    name = name or str(hash(str(g)))

    dot = ['graph ', name, ' {\n']

    for v1, v2, w in g.edges:
        dot += [to_str(v1), ' -- ', to_str(v2)]

        if w != 1 or force_weight:
            dot.append(f' [label="{str(w)}"]')

        dot.append(';\n')

    for v in g.vertices:
        if len(g.neighbors(v)) == 0:
            dot += [to_str(v), ';']

    dot.append('}')

    return ''.join(dot)


def export_dot(g: Graph, filename: str):
    dot = to_dot(g)

    with open(filename, 'w') as file:
        file.write(dot)


def export_png(g: Graph, filename: str, command: str = None):
    dot = to_dot(g)

    if not command:
        if g.is_tree():
            command = Filter.DOT
        elif g.is_complete():
            command = Filter.CIRCO
        else:
            command = Filter.SFDP

    proc = run([command, '-Tpng'], input=dot.encode('utf-8'),
               stdout=PIPE, check=True)

    with open(filename, 'wb') as file:
        file.write(proc.stdout)
