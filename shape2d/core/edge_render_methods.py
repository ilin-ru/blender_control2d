from mathutils import Vector

from ...my_types import TNumber, TVector2D


def line_render(verts: list[Vector], close: bool = True) -> list[tuple[int, int]]:
    edges = []
    length = len(verts) - 1

    for i in range(length + 1):
        if i >= length and close:
            vert = (i, 0)
        else:
            vert = (i, i + 1)

        edges.append(vert)

    return edges


def _grid_render(edges: list[TVector2D]):
    length = len(edges) - 1
    for i in range(length):
        edges.append((i, length - i))

    return edges


def grid_render(verts: list[Vector]):
    return _grid_render(line_render(verts=verts))
