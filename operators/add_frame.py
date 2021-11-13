from bpy_types import Menu
from ..config import Config
from ..utils.create_frame import create_shape
from bpy_extras.object_utils import AddObjectHelper
from bpy.props import FloatVectorProperty
from bpy.types import Operator


class OBJECT_OT_add_shape(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = f"{Config.addon_short_name}.add_shape"
    bl_label = "Add Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="Scale",
        default=(1.0, 1.0, 0),
        subtype='TRANSLATION',
        description="Scale",
    )

    def execute(self, context):
        create_shape(self, context)

        return {'FINISHED'}


def add_shape_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_shape.bl_idname,
        text="Add Shape",
        icon='PLUGIN')


class ShapeKeyControlsMenu(Menu):
    bl_idname = "OBJECT_MT_select_test"
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.select_all",
                        text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")


def shape_key_controls_menu(self, context):
    self.layout.menu('object.select_all', 'test')
    self.layout.operator("object.select_all",
                         text="Select/Deselect All").action = 'TOGGLE'
    self.layout.operator("object.select_all", text="Inverse").action = 'INVERT'
    self.layout.operator("object.select_random", text="Random")

    self.layout.operator(
        OBJECT_OT_add_shape.bl_idname,
        text="Add Shape",
        icon='PLUGIN')
