from ..controls2d.slider import create_slider
from ..config import Config
from ..shape2d.core.edge_render_methods import grid_render
from bpy_extras.object_utils import AddObjectHelper
from bpy.types import Operator


class OBJECT_OT_add_control(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = f"{Config.addon_short_name}.add_control"
    bl_label = "Add Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_slider(context)
        return {'FINISHED'}


def add_control_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_control.bl_idname,
        text="Add control",
        icon='PLUGIN')
