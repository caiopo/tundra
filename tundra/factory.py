from itertools import product
from math import sqrt
from typing import Iterable, Optional, Union

from tundra import Graph, Vertex

__all__ = ('complete', 'biclique', 'crown', 'lattice', 'binary_tree')

IterOrInt = Union[Iterable[Vertex], int]


def complete(iter_or_int: IterOrInt) -> Graph:
    vertices = set(_int_to_range(iter_or_int))

    return Graph(
        vertices,
        {
            (min(v1, v2), max(v1, v2))
            for v1, v2 in product(vertices, vertices)
            if v1 is not v2
        }
    )


def biclique(iter_or_int1: IterOrInt, iter_or_int2: IterOrInt) -> Graph:
    vertices1 = set(_int_to_range(iter_or_int1))
    vertices2 = set(_int_to_range(iter_or_int2))

    return Graph(
        vertices1 | vertices2,
        product(vertices1, vertices2)
    )


def crown(
    iter_or_int1: Iterable[Vertex],
    iter_or_int2: Iterable[Vertex],
) -> Graph:
    vertices1 = list(_int_to_range(iter_or_int1))
    vertices2 = list(_int_to_range(iter_or_int2))

    if len(vertices1) == 0 or len(vertices2) == 0:
        raise ValueError(
            'groups cannot be empty'
        )

    if len(vertices1) != len(vertices2):
        raise ValueError(
            'both groups must be equal in size. '
            f'got: len(iter_or_int1) = {len(vertices1)} and '
            f'len(iter_or_int2) = {len(vertices2)}'
        )

    g = biclique(vertices1, vertices2)

    for v1, v2 in zip(vertices1, vertices2):
        g.unlink(v1, v2)

    return g


def lattice(iter_or_int: IterOrInt = None,
            *,
            width: Optional[int] = None,
            height: Optional[int] = None) -> Graph:
    if iter_or_int is None:
        if width is None or height is None:
            raise ValueError(
                'if iter_or_int is None, width and height must be provided.'
            )

        iter_or_int = width * height

    vertices = list(_int_to_range(iter_or_int))

    if len(vertices) == 0:
        raise ValueError(
            'iterable is empty'
        )

    width, height = _discover_width_and_height(
        len(vertices), width, height
    )

    matrix = [vertices[i:i + width] for i in range(0, len(vertices), width)]

    transposed = [list(z) for z in zip(*matrix)]

    edges = _parallel_edges(matrix) | _parallel_edges(transposed)

    return Graph(
        vertices,
        edges
    )


def binary_tree(iter_or_int: IterOrInt) -> Graph:
    vertices = list(_int_to_range(iter_or_int))

    if len(vertices) == 0:
        raise ValueError(
            'tree cannot be empty'
        )

    g = Graph(vertices)

    for i, _ in enumerate(vertices):
        for offset in {1, 2}:
            j = i * 2 + offset

            if j < len(vertices):
                g.link(
                    vertices[i],
                    vertices[j],
                )

    return g


def _int_to_range(iter_or_int):
    if isinstance(iter_or_int, int):
        return range(iter_or_int)

    return iter_or_int


def _discover_width_and_height(len_, width, height):
    if (width is not None and width <= 0 or
            height is not None and height <= 0):
        raise ValueError(
            'width and height must be greater than zero.'
        )

    if width is None:
        if height is None:
            root = int(sqrt(len_))

            if root**2 == len_:
                return root, root
            else:
                raise ValueError(
                    'if width and height are not specified, '
                    'the iterable size must be a perfect square. '
                    f'it was: {len_}'
                )
        else:
            if len_ % height == 0:
                return len_ // height, height
            else:
                raise ValueError(
                    'cannot create a square with sides '
                    f'{height} and {len_ % height}.'
                )

    else:
        if height is None:
            if len_ % width == 0:
                return width, len_ // width
            else:
                raise ValueError(
                    'cannot create a square with sides '
                    f'{height} and {len_ % width}.'
                )
        else:
            if len_ != height * width:
                raise ValueError(
                    f'cannot create a square with area {len_} and sides '
                    f'{width} and {height}.'
                )

    return width, height


def _parallel_edges(matrix):
    return {edge for line in matrix for edge in zip(line[:-1], line[1:])}
