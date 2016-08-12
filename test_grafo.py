import unittest

from grafo import Grafo

MAX_N = 100

class GrafoTest(unittest.TestCase):
    def test_adiciona_vertice(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            self.assertIn(i, g.vertices(),
                'i deveria pertencer ao grafo')

    def test_remove_vertice(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            g.remove_vertice(i)

        self.assertEqual(g.ordem(), 0,
            'o grafo deveria estar vazio')

    def test_remove_raises(self):
        with self.assertRaises(KeyError,
            msg='remover um vertice inexistente deveria gerar uma exception'):

            Grafo().remove_vertice(0)

    def test_conecta(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            g.conecta(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertIn((i + 1) % MAX_N, g.adjacentes(i),
                'estes vértices deveriam estar conectados')

            self.assertIn(i, g.adjacentes((i + 1) % MAX_N),
                'estes vértices deveriam estar conectados')

    def test_conecta_raises(self):
        with self.assertRaises(KeyError,
            msg='conectar vértices inexistentes deveria gerar uma exception'):
            Grafo().conecta(0, 1)

    def test_desconecta(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            g.conecta(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            g.desconecta((i + 1) % MAX_N, i)

        for i in range(MAX_N):
            self.assertNotIn(i, g.adjacentes(i),
                'estes vértices não deveriam estar conectados')

    def test_desconecta_raises(self):
        with self.assertRaises(KeyError,
            msg='desconectar vértices inexistentes deveria gerar uma exception'):
            Grafo().desconecta(0, 1)

    def test_ordem(self):
        g = Grafo()

        self.assertEqual(g.ordem(), 0)

        for i in range(MAX_N):
            g.adiciona_vertice(i)
            self.assertEqual(g.ordem(), i+1,
                'ordem deveria ser igual ao número de vértices no grafo')

    def test_vertices(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        vertices = g.vertices()

        for i in range(MAX_N):
            self.assertIn(i, vertices,
                '{} deveria ser um elemento de {}'.format(i, vertices))

    def test_um_vertice(self):
        g = Grafo()

        g.adiciona_vertice(0)

        self.assertEqual(g.um_vertice(), 0)

    def test_adjacentes(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            g.conecta(i, (2 * i) % MAX_N)
            g.conecta(i, (3 * i) % MAX_N)
            g.conecta(i, (4 * i) % MAX_N)

        for i in range(MAX_N):
            adj = g.adjacentes(i)

            self.assertIn((2 * i) % MAX_N, adj)
            self.assertIn((3 * i) % MAX_N, adj)
            self.assertIn((4 * i) % MAX_N, adj)

    def test_grau(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            self.assertEqual(g.grau(i), 0)

        for i in range(MAX_N):
            g.conecta(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertEqual(g.grau(i), 2)

        for i in range(MAX_N):
            g.conecta(i, (i + 2) % MAX_N)

        for i in range(MAX_N):
            self.assertEqual(g.grau(i), 4)

    def test_regular(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        self.assertTrue(g.eh_regular())

        g.conecta(0, 1)

        self.assertFalse(g.eh_regular())

        for i in range(1, MAX_N):
            g.conecta(i, (i + 1) % MAX_N)

        self.assertTrue(g.eh_regular())

        g.conecta(1, 3)

        self.assertFalse(g.eh_regular())

    def test_completo(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        self.assertFalse(g.eh_completo())

        for i in range(MAX_N):
            for j in range(MAX_N):
                g.conecta(i, j)

        self.assertFalse(g.eh_completo())

        for i in range(MAX_N):
            g.desconecta(i, i)

        self.assertTrue(g.eh_completo())

    def test_conexo(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        self.assertFalse(g.eh_conexo(),
            'não deveria ser conexo')

        for i in range(0, MAX_N, 2):
            g.conecta(i, i+1)

        self.assertFalse(g.eh_conexo(),
            'não deveria ser conexo')

        for i in range(1, MAX_N, 2):
            g.conecta(i, (i + 1) % MAX_N)

        self.assertTrue(g.eh_conexo(),
            'deveria ser conexo')

    def test_arvore_true(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            if (2 * i + 1) < MAX_N:
                g.conecta(i, 2 * i + 1)

            if (2 * i + 2) < MAX_N:
                g.conecta(i, 2 * i + 2)

        self.assertTrue(g.eh_arvore(), 'deveria ser uma árvore')

    def test_arvore_false(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            g.conecta(i, (i + 1) % MAX_N)

        self.assertFalse(g.eh_arvore(), 'não deveria ser uma árvore')

    def test_fecho_transitivo(self):
        g = Grafo()

        for i in range(MAX_N):
            g.adiciona_vertice(i)

        for i in range(MAX_N):
            self.assertEqual(len(g.fecho_transitivo(i)), 1)

        for i in range(0, MAX_N, 2):
            g.conecta(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertEqual(len(g.fecho_transitivo(i)), 2)

        for i in range(1, MAX_N, 2):
            g.conecta(i, (i + 1) % MAX_N)

        for i in range(MAX_N):
            self.assertEqual(len(g.fecho_transitivo(i)), g.ordem())

if __name__ == '__main__':
    unittest.main()
