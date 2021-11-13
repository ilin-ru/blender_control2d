import bpy
from mathutils import Vector

from ...my_types import TNumber, TVector2D
from ...utils.geometry import create_edges, vertices_apply_scale
from .edge_render_methods import line_render


class Line:
    _verts: list[Vector]
    _name: str
    _is_close: bool = False

    def __init__(self, name: str = 'Line2D') -> None:
        self._verts = []
        self._name = name

    def to(self, x: TNumber, y: TNumber):
        self._verts.append(Vector((x, y, 0)))

    def close(self):
        self._is_close = True

    def to_mesh(self, scale: TVector2D = None, render_method=None):
        if render_method is None:
            render_method = line_render

        if scale is None:
            scale = (1, 1)

        verts = vertices_apply_scale(self._verts, scale)
        edges = render_method(verts)
        faces: list[tuple] = []

        mesh = bpy.data.meshes.new(name=self._name)
        mesh.from_pydata(verts, edges, faces)

        return mesh
