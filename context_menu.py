import bpy
from bpy.types import Menu, ShapeKey


def dump(obj, text):
    for attr in dir(obj):
        print("%r.%s = %s" % (obj, attr, getattr(obj, attr)))


class WM_OT_button_context_test(bpy.types.Operator):
    """Right click entry test"""
    bl_idname = "wm.button_context_test"
    bl_label = "Add control"

    @classmethod
    def poll(cls, context):
        return isinstance(getattr(context, "button_pointer", None), ShapeKey)

    def execute(self, context):
        value = getattr(context, "button_pointer", None)

        if isinstance(value, ShapeKey):
            f = value.driver_add('value')
            f.driver.variables.new()

        # if value is not None:
        #     dump(value, "button_pointer")

        return {'FINISHED'}


# This class has to be exactly named like that to insert an entry in the right click menu
class WM_MT_button_context(Menu):
    bl_label = "Unused"

    def draw(self, context):
        pass


def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(WM_OT_button_context_test.bl_idname)


classes = (
    WM_OT_button_context_test,
    WM_MT_button_context,
)


# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)
#     bpy.types.WM_MT_button_context.append(menu_func)


# def unregister():
#     for cls in classes:
#         bpy.utils.unregister_class(cls)
#     bpy.types.WM_MT_button_context.remove(menu_func)


# if __name__ == "__main__":
#     register()
