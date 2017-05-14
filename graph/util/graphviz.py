from graph import Graph
from os import remove
from os.path import splitext
from subprocess import run, PIPE
from tempfile import mkstemp
from enum import Enum


class Filter(Enum):
    DOT = 'dot'
    NEATO = 'neato'
    TWOPI = 'twopi'
    CIRCO = 'circo'
    FDP = 'fdp'
    SFDP = 'sfdp'
    PATCHWORK = 'patchwork'


def to_dot(g: Graph, name: str = 'graphname') -> str:
    edges = g.edges

    dot = 'graph ' + name + ' {\n'

    for v1, v2, w in edges:
        dot += str(v1) + ' -- ' + str(v2)

        if w != 1:
            dot += str(w)

        dot += ';\n'

    dot += '}'

    return dot


def export_dot(g: Graph, filename: str):
    graphname = splitext(filename)[0]

    dot = to_dot(g)

    with open(filename, 'w') as file:
        file.write(dot)


def export_png(g: Graph, filename: str, command: Filter = None):
    _, tempname = mkstemp(text=True)

    export_dot(g, tempname)

    if not command:
        if g.is_tree():
            command = Filter.DOT
        elif g.is_complete():
            command = Filter.CIRCO
        else:
            command = Filter.FDP

    print(command)
    proc = run([command.value, '-Tpng', tempname], stdout=PIPE)

    print(proc.returncode)

    with open(filename, 'wb') as file:
        file.write(proc.stdout)

    remove(tempname)
