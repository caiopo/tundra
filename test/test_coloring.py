from context import Graph, coloring, complete


def test_coloring_complete():
    for i in range(21):
        g = complete(i)

        n_colors = len({c for _, c in coloring(g).items()})

        assert n_colors == i


def test_coloring_sparse():
    assert len(coloring(Graph())) == 0

    for i in range(1, 21):
        g = Graph(range(i))

        n_colors = len({c for _, c in coloring(g).items()})

        assert n_colors == 1
