import unittest

from grafo import Grafo

MAX_N = 100

class GrafoTest(unittest.TestCase):
    def setUp(self):
        self.g = Grafo()

        for i in range(MAX_N):
            self.g.adiciona_vertice(i)

    def test_adiciona_vertice(self):
        for i in range(MAX_N):
            self.assertIn(i, self.g.vertices(),
                'i deveria pertencer ao grafo')

    def test_remove_vertice(self):
        for i in range(MAX_N):
            self.g.remove_vertice(i)

        self.assertEqual(self.g.ordem(), 0,
            'o grafo deveria estar vazio')

    def test_remove_raises(self):
        with self.assertRaises(KeyError,
            msg='remover um vertice inexistente deveria gerar uma exception'):

            Grafo().remove_vertice(0)

    def test_conecta(self):
        for i in range(MAX_N):
            self.g.conecta(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertIn((i + 1) % MAX_N, self.g.adjacentes(i),
                'estes vértices deveriam estar conectados')

            self.assertIn(i, self.g.adjacentes((i + 1) % MAX_N),
                'estes vértices deveriam estar conectados')

    def test_conecta_raises(self):
        with self.assertRaises(KeyError,
            msg='conectar vértices inexistentes deveria gerar uma exception'):
            Grafo().conecta(0, 1)

    def test_desconecta(self):
        for i in range(MAX_N):
            self.g.conecta(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.g.desconecta((i + 1) % MAX_N, i)

        for i in range(MAX_N):
            self.assertNotIn(i, self.g.adjacentes(i),
                'estes vértices não deveriam estar conectados')

    def test_desconecta_raises(self):
        with self.assertRaises(KeyError,
            msg='desconectar vértices inexistentes deveria gerar uma exception'):
            Grafo().desconecta(0, 1)

    def test_ordem(self):
        gr = Grafo()

        self.assertEqual(gr.ordem(), 0,
            'ordem deveria ser igual ao número de vértices no grafo')

        for i in range(MAX_N):
            gr.adiciona_vertice(i)
            self.assertEqual(gr.ordem(), i+1,
                'ordem deveria ser igual ao número de vértices no grafo')

    def test_vertices(self):
        vertices = self.g.vertices()

        for i in range(MAX_N):
            self.assertIn(i, vertices,
                '{} deveria ser um elemento de {}'.format(i, vertices))

    def test_um_vertice(self):
        gr = Grafo()

        gr.adiciona_vertice(0)

        self.assertEqual(gr.um_vertice(), 0)

        gr.remove_vertice(0)

        gr.adiciona_vertice(1)

        self.assertEqual(gr.um_vertice(), 1)

    def test_adjacentes(self):
        for i in range(MAX_N):
            self.g.conecta(i, (2 * i) % MAX_N)
            self.g.conecta(i, (3 * i) % MAX_N)
            self.g.conecta(i, (4 * i) % MAX_N)

        for i in range(MAX_N):
            adj = self.g.adjacentes(i)

            self.assertIn((2 * i) % MAX_N, adj)
            self.assertIn((3 * i) % MAX_N, adj)
            self.assertIn((4 * i) % MAX_N, adj)

    def test_grau(self):
        for i in range(MAX_N):
            self.assertEqual(self.g.grau(i), 0)

        for i in range(MAX_N):
            self.g.conecta(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertEqual(self.g.grau(i), 2)

        for i in range(MAX_N):
            self.g.conecta(i, (i + 2) % MAX_N)

        for i in range(MAX_N):
            self.assertEqual(self.g.grau(i), 4)

    def test_regular(self):
        self.assertTrue(self.g.eh_regular())

        self.g.conecta(0, 1)

        self.assertFalse(self.g.eh_regular())

        for i in range(1, MAX_N):
            self.g.conecta(i, (i + 1) % MAX_N)

        self.assertTrue(self.g.eh_regular())

        self.g.conecta(1, 3)

        self.assertFalse(self.g.eh_regular())

    def test_completo(self):
        self.assertFalse(self.g.eh_completo())

        for i in range(MAX_N):
            for j in range(MAX_N):
                self.g.conecta(i, j)

        self.assertFalse(self.g.eh_completo())

        for i in range(MAX_N):
            self.g.desconecta(i, i)

        self.assertTrue(self.g.eh_completo())

    def test_conexo(self):
        self.assertFalse(self.g.eh_conexo(),
            'não deveria ser conexo')

        for i in range(0, MAX_N, 2):
            self.g.conecta(i, i+1)

        self.assertFalse(self.g.eh_conexo(),
            'não deveria ser conexo')

        for i in range(1, MAX_N, 2):
            self.g.conecta(i, (i + 1) % MAX_N)

        self.assertTrue(self.g.eh_conexo(),
            'deveria ser conexo')

    def test_arvore_true(self):
        for i in range(MAX_N):
            if (2 * i + 1) < MAX_N:
                self.g.conecta(i, 2 * i + 1)

            if (2 * i + 2) < MAX_N:
                self.g.conecta(i, 2 * i + 2)

        self.assertTrue(self.g.eh_arvore(), 'deveria ser uma árvore')

    def test_arvore_false(self):
        for i in range(MAX_N):
            self.g.conecta(i, (i + 1) % MAX_N)

        self.assertFalse(self.g.eh_arvore(), 'não deveria ser uma árvore')

    def test_fecho_transitivo(self):
        for i in range(MAX_N):
            self.assertEqual(self.g.fecho_transitivo(i), {i})

        for i in range(0, MAX_N, 2):
            self.g.conecta(i, (i + 1) % MAX_N)

        for i in range(0, MAX_N, 2):
            self.assertEqual(self.g.fecho_transitivo(i), {i, (i + 1) % MAX_N})

        for i in range(1, MAX_N, 2):
            self.assertEqual(self.g.fecho_transitivo(i), {i - 1, i})

        for i in range(1, MAX_N, 2):
            self.g.conecta(i, (i + 1) % MAX_N)

        self.assertTrue(self.g.eh_conexo())

        for i in range(MAX_N):
            self.assertEqual(self.g.fecho_transitivo(i), self.g.vertices())

if __name__ == '__main__':
    unittest.main()
