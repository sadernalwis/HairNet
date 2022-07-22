import bpy
from mathutils import Quaternion, Vector
from math import pi
from bpy.props import IntProperty, FloatProperty


bl_info = {
    "name": "Coil Curve Gen",
    "author": "Phil Cote, cotejrp1",
    "version": (0, 0, 1),
    "blender": (3, 2, 0),
    "location": "View3D > Add > Curve",
    "description": "Add a coiled bezier curve to the scene.",
    "warning": "",
    "category": "Add Curve"}


def get_mesh_data(rad=5, point_count=10, turn_width=.5, turn_height=0.0, points_per_turn=5, h_taper=0.0, w_taper=0.0):    
    axis = [0,0,-1]
    cur_z = 0
    PI_2 = pi * 2
    ppt = points_per_turn-1
    num_of_turns = 0
    point_count -= 1 #offset for the one point already in the new curve.
    x_vals = [x for x in range(1, point_count+2)]
    x_vals = [(x/ppt)*PI_2 for x in x_vals]
    quats = [Quaternion(axis, x) for x in x_vals]
    
    def taper_values(turn_factor, taper): #Adjust heights or widths for tapering as needed
        new_list = []
        for i, q in enumerate(quats):
            if i % points_per_turn == 0: turn_factor -= taper
            new_list.append(turn_factor)
        return new_list    
    turn_heights = taper_values(turn_height, h_taper)
    turn_widths = taper_values(turn_width, w_taper)
    vecs = []
    for i, q in enumerate(quats):
        vec = q @ Vector((rad,0,cur_z))
        vecs.append(vec)
        rad+=turn_widths[i]
        cur_z+=turn_heights[i]
    coords = [(v.x,v.y,v.z) for v in vecs]
    return coords


class QuatOperator(bpy.types.Operator):
    bl_idname = "mesh.primitive_quat_add"
    bl_label = "Add Quat"
    bl_options = {'REGISTER', 'UNDO'}
    pc : IntProperty( name = "Point Count", description = "Point Count", min = 3, max = 50, default = 5)
    radius : FloatProperty( name = "Radius", description = "Radius", min = .1, max = 10, default = 1)
    turn_width : FloatProperty(name="Turn Width", min = -1.0, max=1.0, default=0)
    turn_height : FloatProperty(name="Turn Height", min=-1.0, max=1.0,default=0)
    points_per_turn : IntProperty(name="Points Per Turn", min=3,max=30,default=5)
    h_taper : FloatProperty(name="Height Taper", min=-1, max=1,default=0, description="How much to decrease each turn height", )
    w_taper : FloatProperty(name="Width Taper", min=-1, max=1,default=0, description="How much to decrease each turn height", )
    
    def execute(self, context):
        mesh_data = get_mesh_data(rad=self.radius,  # set up the mesh data to be more suitable for curve objects.
                                  point_count=self.pc,
                                  turn_width=self.turn_width,
                                  turn_height=self.turn_height,
                                  points_per_turn=self.points_per_turn,
                                  h_taper=self.h_taper, w_taper=self.w_taper)
        flat_list = []
        for md in mesh_data: flat_list.extend(md)
        crv = bpy.data.curves.new("crv", type="CURVE") # build the curve
        spln = crv.splines.new(type="BEZIER")
        points = spln.bezier_points
        points.add(self.pc-1)
        points.foreach_set("co", flat_list)
        for i, point in enumerate(points):
            if i > 0: point.handle_left_type = point.handle_right_type = "AUTO"
        ob = bpy.data.objects.new("quat_ob", crv)        
        bpy.context.scene.collection.objects.link(ob)
        return {'FINISHED'}
        
def menu_func(self, context):
    self.layout.operator(QuatOperator.bl_idname, text="Add Coil Curve", icon = "PLUGIN")

def register():
    bpy.utils.register_class(QuatOperator)
    bpy.types.VIEW3D_MT_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(QuatOperator)
    bpy.types.VIEW3D_MT_add.remove(menu_func)

if __name__ == "__main__":
    register()

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
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

# original source: https://gist.github.com/pcote/2648286