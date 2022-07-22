import logging, numpy as np, bpy, mathutils, math
from math import cos, degrees, radians, sin
from mathutils import Vector, Matrix
from Utilities.Utilities import Utilities
logger = logging.getLogger(__name__)

class ObjectOps:
    def get_object_by_name(name):
        return bpy.data.objects.get(name)

    def get_objects(*names):
        return [bpy.data.objects.get(name) for name in names]
    
    def get_active_object():
        return bpy.context.view_layer.objects.active

    def set_active_object(obj):
        if obj: bpy.context.view_layer.objects.active = obj

    def select_object_by_name(name):
        oo = ObjectOps
        obj = oo.get_object_by_name(name)
        if obj: obj.select_set(True)

    def set_selected_objs_by_name(names):
        for name in names:
            if name in bpy.data.objects: bpy.data.objects[name].select_set(True)

    def deselect_all_objects():
        for obj in bpy.data.objects: obj.select_set(False)

    def is_object(obj):
        return isinstance(obj, bpy.types.Object)

    def is_mesh(obj):
        return isinstance(obj, bpy.types.Mesh)

    def get_objects_selected_names():
        selected_objects = []
        for obj in bpy.context.selected_objects:
            if hasattr(obj, 'name'): selected_objects.append(obj.name)
        return selected_objects

    def select_and_change_mode(obj, obj_mode):
        oo = ObjectOps
        oo.deselect_all_objects()
        if type(obj) is str: obj = bpy.data.objects.get(obj)
        if obj:
            obj = obj
            obj.select_set(True)
            oo.set_active_object(obj)
            oo.set_object_visible(obj)
            try:
                bpy.ops.object.mode_set(mode=obj_mode)
                logger.debug("Select and change mode of %s = %s", obj.name, obj_mode)
            except AttributeError:
                logger.warning("Can't change the mode of %s to %s", obj.name, obj_mode)

    def set_object_visible(obj):
        if obj: obj.hide_set(False)

    def get_empty(location=None, name='empty'):
        oo = ObjectOps
        # o = bpy.data.objects.new( "empty", None )
        bpy.ops.object.add() #Add a temporary empty
        empty_obj = oo.get_active_object()
        if location:
            empty_obj.location = location
            bpy.context.scene.cursor.location = location
        oo.set_active_object(empty_obj)
        return empty_obj

    @Utilities.mode('OBJECT', keep=True)
    def get_object(name, else_empty=True):
        oo = ObjectOps
        obj = bpy.data.objects.get(name)
        if not obj and else_empty: obj = oo.get_empty(name=name)
        oo.set_active_object(obj)
        return obj

    @Utilities.mode('OBJECT')
    def delete_object(obj):
        oo = ObjectOps
        oo.select_and_change_mode(obj, "OBJECT")
        # bpy.ops.object.delete()
        bpy.ops.object.delete({"selected_objects": [obj]})
        bpy.context.view_layer.update()

    def evaluated(depsgraph, obj, modifier_name=None, particle_system=False):
        retval = [None, None, None]
        retval[0] = obj.evaluated_get(depsgraph)
        if modifier_name:   retval[1] = retval[0].modifiers[modifier_name]
        if particle_system: retval[2] = retval[1].particle_system
        return retval
        
    def safe_remove(obj):
        try:
            collections = obj.users_collection
            for c in collections: c.objects.unlink(obj)
            if(obj.data.users == 1):
                if(obj.type == 'MESH'): bpy.data.meshes.remove(obj.data)
                elif(obj.type == 'CURVE'): bpy.data.curves.remove(obj.data)
                #else? TODO
            bpy.data.objects.remove(obj)
        except:
            pass

# MB-Lab
#
# MB-Lab fork website : https://github.com/animate1978/MB-Lab
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#
# ManuelbastioniLAB - Copyright (C) 2015-2018 Manuel Bastioni
