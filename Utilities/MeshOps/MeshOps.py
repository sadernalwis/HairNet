import logging, bpy, bmesh, sys, os
from ...Utilities.Utilities import Utilities
from ...Utilities.ObjectOps.ObjectOps import ObjectOps as oo
logger = logging.getLogger(__name__)

class MeshOps:
    def new_mesh(name, matrix=None):
        mesh = bpy.data.meshes.new(name=name)
        obj = bpy.data.objects.new(name, mesh)
        if matrix: obj.matrix_world = matrix
        bpy.context.scene.collection.objects.link(obj)
        return obj, mesh
    
    def update_VEF(mesh, Vs=[], Es=[], Fs=[]):
        # mesh = obj.data
        mesh.from_pydata(Vs, Es, Fs)
        mesh.update()
    
    def select_stems(obj, stems):
        bpy.ops.object.mode_set(mode='OBJECT')
        mesh = obj.data
        root_index = 0
        for steps in stems:
            mesh.vertices[root_index].select = True
            root_index += steps
        
    def deselect_Vs(obj):
        oo.select_and_change_mode(obj, 'EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='DESELECT')

    def seamed_Es(obj):
        return [e for e in obj.data.edges if e.use_seam]

    def unique_EV(Es):
        unique_Vs = [] 
        for e in Es:
            for v in e.vertices:
                if v not in unique_Vs: unique_Vs.append(v)
        return unique_Vs

    def Es_with_v(E, v):
        return [e_x for e_x in E if v in e_x.key]

    def reorder_EVs(E, V): # x_ : tried xs, _x : used xs
        mo = MeshOps
        v_sorted, _e =  [],[]
        for v in V:
            e = mo.Es_with_v(E, v)[0]
            v_sorted.append(v)
            run = True
            while run:
                for ev in e.key: # edgepoint
                    if v != ev: #we have found the other vert if this e store it and find the next e
                        v = ev
                        v_sorted.append(v)
                        _e.append(e)
                        break
                try:
                    e = [e_x for e_x in E if ((v in e_x.key) and (e_x not in _e))][0]
                except:
                    run = False
        return v_sorted

    def sort_seam(V, E):  # x_ : tried xs, _x : used xs
        v_, e_, v_origin =  [],[],[]
        def get_endpoint(vert): #Make a list of starting points so that each island will have a starting point. Make another "used E" list
            for v in V:
                if v not in v_:
                    v_.append(v)
                    all_edges = [e for e in E if v in e.vertices] #get all E with v in it
                    if len(all_edges) == 1:
                        v_origin.append(v) #The vert is in only one edge and is thus an endpoint
                        walking = True #walk to the other end of the seam and add V to v_
                        v_last = v
                        edge_start = edge_last = all_edges[0]
                        while walking:
                            if v_last == edge_last.key[0]: v_last = edge_last.key[1]
                            else: v_last = edge_last.key[0]
                            e_.append(edge_last)
                            if v_last not in v_: v_.append(v_last)
                            edge_next = [e for e in E if v_last in e.vertices and e not in e_]
                            if len(edge_next) == 1: edge_last = edge_next[0]
                            else: walking = False
            return edge_start, v
        for v in V:
            if v not in v_: edge, vn = get_endpoint(v)
        return MeshOps.reorder_EVs(E, v_origin)

    def seams_VE(obj):
        mo = MeshOps
        error = 0
        seamed_Es = mo.seamed_Es(obj)
        seamed_Vs = mo.unique_EV(seamed_Es)
        if(len(seamed_Es) < 2): return 0, 0, 2
        seamed_Vs = mo.sort_seam(seamed_Vs, seamed_Es)
        return seamed_Vs, seamed_Es, (2 if len(seamed_Es) == 0 else error)
