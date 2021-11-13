import math
import bpy

from bpy_types import PoseBone
from ..my_types import TNumber, TVector2D

from ..shape2d import ShapeFactory, edge_render_methods
from . import Control


def create_control(context, silder_offset: TNumber = .2, size: TVector2D = (.3, 1)):
    root_size_x, root_size_y = size
    silder_size_y = root_size_x
    root_size_y += silder_size_y * 2

    root_fac = ShapeFactory()
    root_fac.rotate = (0, 0, math.pi / 2)
    root_fac.translate = (0, root_size_y / 2, 0)

    root_shape = root_fac.create_rouded_box(
        root_size_x, root_size_y / 2 - root_size_x)

    slider_fac = ShapeFactory()
    slider_fac.translate = (0, 1, 0)
    slider_shape = slider_fac.create_arc(
        math.pi * 2, segment_count=20, render_method=edge_render_methods.grid_render, radius=1 - silder_offset)

    control = Control(control_type='slider')

    root = control.add_bone('root', 0, 0)
    slider = control.add_bone('slider', 0,
                              0, silder_size_y)

    control.set_parent(root, slider)
    control.set_shape(root, root_shape)
    control.set_shape(slider, slider_shape)

    return control, slider, root


def create_constraint(bone: PoseBone):
    constraint = bone.constraints.new(type='LIMIT_LOCATION')
    constraint.use_min_x = True
    constraint.use_min_y = True
    constraint.use_min_z = True

    constraint.use_max_x = True
    constraint.use_max_y = True
    constraint.use_max_z = True

    constraint.max_y = 1

    constraint.use_transform_limit = True
    constraint.owner_space = 'LOCAL'

    return constraint


def create_slider(context, silder_offset: TNumber = .2, size: TVector2D = (.3, 1), name: str = None) -> Control:
    control, slider, root = create_control(context, silder_offset, size)
    bones = control.get_pose_bones()

    text_fac = ShapeFactory()
    text = text_fac.create_text(slider + '_text', name)
    text.rotation_euler = (math.pi / 2, 0, 0)
    # text.location = (0, 0, -size[1] / 2)
    text.data.align_x = 'CENTER'
    text.data.fill_mode = 'NONE'
    text.data.size = size[1] / 2
    text.data.offset = .006

    constraint = text.constraints.new('CHILD_OF')
    constraint.target = control.get_object()
    constraint.subtarget = root

    create_constraint(bones.get(slider))

    control.get_object().name = 'Slider'
    control.get_object()['slider_bone'] = control.get_bone_id('slider')
    control.get_object().location = bpy.context.scene.cursor.location
    arr = list(context.scene.cursor.location)
    arr[2] = arr[2] - size[1] / 2
    text.location = tuple(arr)

    return control
