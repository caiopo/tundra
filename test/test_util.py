import unittest
from subprocess import PIPE, run
from tempfile import NamedTemporaryFile

from context import Graph, export_dot, export_png, to_dot

g_dot1 = 'graph .* {\n"1" -- "2";\n"0" -- "1";\n"5" -- "6";\n' \
    '"6" -- "7";\n"8" -- "9";\n"3" -- "4";\n"7" -- "8";\n"4" -- "5";' \
    '\n"2" -- "3";\n}'

g_dot2 = 'graph .* {\n"1" -- "2";\n"0" -- "1";\n"5" -- "6";\n' \
         '"6" -- "7";\n"3" -- "4";\n"7" -- "8";\n"4" -- "5";\n"2" -- "3";\n"9";}'

g_dot_weighted = '''
graph {} {{\n"2" -- "3" [label="5"];\
\n"7" -- "8" [label="5"];\n"8" -- "9" [label="5"];\
\n"6" -- "7" [label="5"];\n"4" -- "5" [label="5"];\
\n"5" -- "6" [label="5"];\n"3" -- "4" [label="5"];\
\n"1" -- "2" [label="5"];\n"0" -- "1" [label="5"];\n}}
'''.strip()


def is_png(filename):
    result = run(['file', '--mime-type', filename], stdout=PIPE, check=True)

    return result.stdout.decode('utf-8').split()[1] == 'image/png'


class TestGraphviz(unittest.TestCase):
    def setUp(self):
        self.g = Graph(range(10), zip(range(9), range(1, 10)))

    def test_to_dot(self):
        self.assertRegex(to_dot(self.g), g_dot1)

        self.g.unlink(8, 9)

        self.assertRegex(to_dot(self.g), g_dot2)

    def test_weighted_dot(self):
        g = Graph(range(10), zip(range(9), range(1, 10), [5] * 9))

        self.assertEqual(to_dot(g), g_dot_weighted.format(hash(str(g))))

    def test_export_dot(self):
        with NamedTemporaryFile() as file:
            export_dot(self.g, file.name)

            self.assertRegex(file.read().decode('utf-8'), g_dot1)

        self.g.unlink(8, 9)

        with NamedTemporaryFile() as file:
            export_dot(self.g, file.name)

            self.assertRegex(file.read().decode('utf-8'), g_dot2)

    def test_export_png(self):
        with NamedTemporaryFile() as file:
            export_png(self.g, file.name)

            self.assertTrue(is_png(file.name))

        for v1 in self.g.vertices:
            for v2 in self.g.vertices:
                if v1 != v2:
                    self.g.link(v1, v2)

        self.assertTrue(self.g.is_complete())

        with NamedTemporaryFile() as file:
            export_png(self.g, file.name)

            self.assertTrue(is_png(file.name))

        self.g.unlink(0, 1)

        with NamedTemporaryFile() as file:
            export_png(self.g, file.name)

            self.assertTrue(is_png(file.name))
