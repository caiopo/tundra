from subprocess import PIPE, run
from tempfile import NamedTemporaryFile

import pytest

from context import Graph, export_dot, export_png, is_complete, to_dot

g_dot1 = 'graph {\n"1" -- "2";\n"0" -- "1";\n"5" -- "6";\n' \
    '"6" -- "7";\n"8" -- "9";\n"3" -- "4";\n"7" -- "8";\n"4" -- "5";' \
    '\n"2" -- "3";\n}'

g_dot2 = 'graph {\n"1" -- "2";\n"0" -- "1";\n"5" -- "6";\n' \
         '"6" -- "7";\n"3" -- "4";\n"7" -- "8";\n"4" -- "5";\n' \
         '"2" -- "3";\n"9";\n}'

g_dot_weighted = '''
graph {\n"2" -- "3" [label="5"];\
\n"7" -- "8" [label="5"];\n"8" -- "9" [label="5"];\
\n"6" -- "7" [label="5"];\n"4" -- "5" [label="5"];\
\n"5" -- "6" [label="5"];\n"3" -- "4" [label="5"];\
\n"1" -- "2" [label="5"];\n"0" -- "1" [label="5"];\n}
'''.strip()

g_dot_color = '''
graph {\n"1" -- "2";\n"0" -- "1";\n"5" -- "6" [color="red"];\
\n"6" -- "7" [color="red"];\n"8" -- "9" [color="red"];\n\
"3" -- "4" [color="red"];\n"7" -- "8" [color="red"];\n\
"4" -- "5" [color="red"];\n"2" -- "3";\n}
'''.strip()


def is_png(filename):
    result = run(['file', '--mime-type', filename], stdout=PIPE, check=True)

    return result.stdout.decode('utf-8').split()[1] == 'image/png'


@pytest.fixture
def g():
    return Graph(range(10), zip(range(9), range(1, 10)))


def test_to_dot(g):
    assert to_dot(g) == g_dot1

    g.unlink(8, 9)

    assert to_dot(g) == g_dot2


def test_weighted_dot(g):
    g = Graph(range(10), zip(range(9), range(1, 10), [5] * 9))

    assert to_dot(g) == g_dot_weighted


def test_color_dot(g):
    g = Graph(range(10), zip(range(9), range(1, 10)))

    def edge_color(v1, v2, w):
        return 'red' if (v1 + v2) > 5 else None

    assert to_dot(g, edge_color=edge_color) == g_dot_color


def test_export_dot(g):
    with NamedTemporaryFile() as file:
        export_dot(g, file.name)

        assert file.read().decode('utf-8') == g_dot1

    g.unlink(8, 9)

    with NamedTemporaryFile() as file:
        export_dot(g, file.name)

        assert file.read().decode('utf-8') == g_dot2


def test_export_png(g):
    with NamedTemporaryFile() as file:
        export_png(g, file.name)

        assert is_png(file.name)

    for v1 in g.vertices:
        for v2 in g.vertices:
            if v1 != v2 and not g.has_edge(v1, v2):
                g.link(v1, v2)

    assert is_complete(g)

    with NamedTemporaryFile() as file:
        export_png(g, file.name)

        assert is_png(file.name)

    g.unlink(0, 1)

    with NamedTemporaryFile() as file:
        export_png(g, file.name)

        assert is_png(file.name)
