import bpy
from bpy.types import Mesh, Object
from mathutils import Matrix, Vector

from ...my_types import TNumber, TVector2D
from .line import Line


def apply_transfrom(ob, use_location=False, use_rotation=False, use_scale=False):
    mb = ob.matrix_basis
    I = Matrix()
    loc, rot, scale = mb.decompose()

    # rotation
    T = Matrix.Translation(loc)
    #R = rot.to_matrix().to_4x4()
    R = mb.to_3x3().normalized().to_4x4()
    S = Matrix.Diagonal(scale).to_4x4()

    transform = [I, I, I]
    basis = [T, R, S]

    def swap(i):
        transform[i], basis[i] = basis[i], transform[i]

    if use_location:
        swap(0)
    if use_rotation:
        swap(1)
    if use_scale:
        swap(2)

    M = transform[0] @ transform[1] @ transform[2]
    if hasattr(ob.data, "transform"):
        ob.data.transform(M)
    for c in ob.children:
        c.matrix_local = M @ c.matrix_local

    ob.matrix_basis = basis[0] @ basis[1] @ basis[2]


class Shape:
    _line: Line
    _name: str
    _rotate: Vector = None
    _translate: Vector = None
    _scale: Vector = None

    def __init__(self, verts: list[TVector2D], name: str = 'Shape2D') -> None:
        self._line = Line(name=name)
        self._name = name
        self._handlers = {}

        for i in verts:
            self._line.to(i[0], i[1])

        self._line.close()

    def rotate(self, x: TNumber, y: TNumber, z: TNumber):
        self._rotate = Vector((x, y, z))
        return self

    def translate(self, x: TNumber, y: TNumber, z: TNumber):
        self._translate = Vector((x, y, z))
        return self

    def scale(self, x: TNumber, y: TNumber, z: TNumber):
        self._scale = Vector((x, y, z))
        return self

    def to_mesh(self, scale: tuple[int, int] = None, render_method=None) -> Mesh:
        mesh = self._line.to_mesh(scale=scale, render_method=render_method)
        return mesh

    def to_object(self, scale: tuple[int, int] = None, render_method=None) -> Object:
        mesh = self.to_mesh(render_method=render_method)
        object = bpy.data.objects.new(self._name, mesh)

        if self._rotate is not None:
            object.rotation_euler = self._rotate
            apply_transfrom(object, use_rotation=True)

        if self._translate is not None:
            object.location = self._translate
            apply_transfrom(object, use_location=True)

        return object
