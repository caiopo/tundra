from random import choice

class Grafo:
    def __init__(self):
        self._vertices = {}

    def adiciona_vertice(self, v):
        """
        Adiciona um novo vértice em G
        """
        self._vertices[v] = set()

    def remove_vertice(self, v):
        """
        Remove um  vértice de G, juntamente com todas as conexões
        """
        for v2 in self._vertices[v]:
            self.desconecta(v, v2)

        del self._vertices[v]

    def conecta(self, v1, v2):
        """
        Conecta os vértices v1 e v2 em G
        """
        self._vertices[v1].add(v2)
        self._vertices[v2].add(v1)

    def desconecta(self, v1, v2):
        """
        Desconecta os vértices v1 e v2 em G
        """
        self._vertices[v1].remove(v2)
        if v1 != v2:
            self._vertices[v2].remove(v1)

    def ordem(self):
        """
        Retorna o número de vértices de G
        """
        return len(self._vertices)

    def vertices(self):
        """
        Retorna um conjunto contendo os vértices de G
        """
        return tuple(self._vertices.keys())

    def um_vertice(self):
        """
        Retorna um vértice qualquer de G
        """
        return choice(self.vertices())

    def adjacentes(self, v):
        """
        Retorna um conjunto contendo os vértices adjacentes a v em G
        """
        return tuple(self._vertices[v])

    def grau(self, v):
        """
        Retorna o número de vértices adjacentes a v em G
        """
        return len(self.adjacentes(v))

    def eh_regular(self):
        """
        Verifica se todos os vértices de G possuem o mesmo grau
        """
        grau = self.grau(self.um_vertice())

        for v in self.vertices():
            if self.grau(v) != grau:
                return False

        return True

    def eh_completo(self):
        """
        Verifica se cada vértice de G está conectados
        a todos os outros vértices
        """
        grau = self.ordem() - 1

        for v in self.vertices():
            if self.grau(v) != grau:
                return False

        return True

    def eh_conexo(self):
        """
        Verifica se existe pelo menos um caminho entre
        cada par de vértices de G
        """
        return (sorted(self.vertices()) ==
                    sorted(self.fecho_transitivo(self.um_vertice())))

    def eh_arvore(self):
        """
        Verifica se não há ciclos em G
        """
        def ha_ciclo_com(v, v_anterior, ja_visitados=None):
            """
            Privado - verifica se v faz parte de algum ciclo no grafo
            """

            ja_visitados = ja_visitados or []

            if v in ja_visitados:
                return True

            ja_visitados.append(v)

            for v_adj in self.adjacentes(v):
                if v_adj != v_anterior:
                    if ha_ciclo_com(v_adj, v, ja_visitados):
                        return True

            ja_visitados.remove(v)

            return False

        v = self.um_vertice()

        return self.eh_conexo() and not ha_ciclo_com(v, v)

    def fecho_transitivo(self, v, ja_visitados=None):
        """
        Retorna um conjunto contendo todos os vértices de G que
        são transitivamente alcancáveis partindo-se de v
        """
        ja_visitados = ja_visitados or []

        ja_visitados.append(v)

        for v_adj in self.adjacentes(v):
            if not v_adj in ja_visitados:
                self.fecho_transitivo(v_adj, ja_visitados)

        return ja_visitados


