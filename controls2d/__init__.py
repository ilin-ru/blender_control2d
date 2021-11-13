import math
from bpy.types import Object, Armature, ArmatureEditBones
from bpy_types import PoseBone
from ..config import Config
from ..utils.increment_id import increment_id
from ..my_types import TNumber

import bpy


class Control:  # Yes, am not like getters(@property). Why? Just not like.
    _arm: Armature
    _arm_obj: Object
    _arm_edit: ArmatureEditBones
    _arm_pose: dict[str, PoseBone]
    _control_id: int
    _bones: dict[str, str]

    def __init__(self, control_type: str) -> None:
        self._arm = bpy.data.armatures.new('Control2DArmature')
        self._arm_obj = bpy.data.objects.new('Control2DObject', self._arm)
        self._arm_edit = self._arm_obj.data.edit_bones
        self._control_id = increment_id()
        self._bones = {}

        self._arm_obj['control_type'] = control_type
        self._arm_obj[Config.addon_short_name] = True

        bpy.context.scene.collection.objects.link(self._arm_obj)
        bpy.context.view_layer.objects.active = self._arm_obj

    def get_pose_bones(self) -> dict[str, PoseBone]:
        bpy.ops.object.mode_set(mode='POSE', toggle=False)
        return self._arm_obj.pose.bones

    def get_edit_bones(self) -> ArmatureEditBones:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        return self._arm_edit

    def get_bone_id(self, name: str) -> str:
        return self._bones[name]

    def get_armature(self):
        return self._arm

    def get_object(self):
        return self._arm_obj

    def set_shape(self, name: str, obj: Object):
        bones = self.get_pose_bones()
        bones[name].custom_shape = obj

    def set_parent(self, name1: str, name2: str):
        bones = self.get_edit_bones()
        bones[name2].parent = bones[name1]

    def add_bone(self, name: str, x1: TNumber, y1: TNumber, h: TNumber = 1):
        n = f'{name}_id_{self._control_id}'
        self._bones[name] = n
        name = n

        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        b = self._arm_edit.new(name)
        b.head = (0, x1, y1)

        if y1 == 0:
            b.tail = (0, x1, 1 * h)
        else:
            b.tail = (0, x1, y1 * h)

        return name
