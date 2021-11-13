bl_info = {
    "name": "Control2D",
    "author": "ilin ru",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "View3D > Add > Mesh",
    "doc_url": "https://github.com/ilin-ru/control2d",
    "tracker_url": "https://github.com/ilin-ru/control2d/issues",
    "warning": "",
    "category": "Add Mesh"
}


from .ui.context_menu import context_menu, object_context_menu
from .operators.add_frame import add_shape_button
from .operators.add_control import add_control_button
from .operators import classes as operators_classes
from . import operators, ui
from bpy.types import StringProperty
import bpy

classes = [*operators.classes, *ui.classes]


def register():
    for i in classes:
        bpy.utils.register_class(i)

    # bpy.types.VIEW3D_MT_mesh_add.append(add_shape_button)
    bpy.types.VIEW3D_MT_mesh_add.append(add_control_button)
    bpy.types.WM_MT_button_context.append(context_menu)
    bpy.types.VIEW3D_MT_object_context_menu.append(object_context_menu)


def unregister():

    bpy.types.WM_MT_button_context.remove(context_menu)

    for i in classes:
        bpy.utils.unregister_class(i)

    # bpy.types.VIEW3D_MT_mesh_add.remove(add_shape_button)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_control_button)
    bpy.types.VIEW3D_MT_object_context_menu.remove(object_context_menu)
    # bpy.types.WM_MT_button_context.remove(context_menu)
