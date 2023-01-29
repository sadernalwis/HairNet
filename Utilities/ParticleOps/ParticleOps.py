import bpy

from ...Utilities.MeshOps.MeshOps import MeshOps as mo
from ...Utilities.ObjectOps.ObjectOps import ObjectOps as oo

class ParticleOps:
    
    def particle_setting(obj, system_name):
        return (obj.particle_systems[system_name].settings, obj.particle_systems[system_name])
    
    def particle_activate(obj, system_name):
        obj.particle_systems.active_index = obj.particle_systems.find(system_name) #Get active_index of desired particle system
        
    def particle_remove(obj, system_name):
        setting, system = ParticleOps.particle_setting(obj, system_name)
        override = {"object": obj, "particle_system": system}
        bpy.ops.object.particle_system_remove(override)

    def particle_delete(obj, system_name):
        setting, system = ParticleOps.particle_setting(obj, system_name)
        ParticleOps.particle_activate(obj, system_name)
        ParticleOps.particle_remove(obj, system_name) #Delete Particle System
        bpy.data.particles.remove(setting) #Delete Particle System Settings

    def settings_copy(system_name):
        return bpy.data.particles[system_name].copy()
    
    def particle_modifier(obj):
        system = obj.particle_systems.active
        modifier = None
        for m in obj.modifiers:
            if m.type == "PARTICLE_SYSTEM" and m.particle_system == system:
                modifier = m
                break
        return (system, modifier)

    def hair_system(obj, system_name):
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.modifiers.new("HairNet", 'PARTICLE_SYSTEM') #Adding a particle modifier also works but requires pushing/pulling the active object and selection.
        # override = {"object": obj, "particle_system": systemName} #Set up context override
        # bpy.ops.object.particle_system_add(override)
        obj.particle_systems[-1].name = system_name
        obj.particle_systems[-1].settings.type = 'HAIR'
        obj.particle_systems[-1].settings.render_step = 5
        return obj.particle_systems[system_name]

    def to_VE(obj_eval, modifier_eval, system, system_eval):
        V ,E = [], []
        hair_steps = []
        for hair_index in range(0, len(system.particles)):
            hair = system.particles[hair_index]
            hair_eval = system_eval.particles[hair_index]
            key_length = len(hair.hair_keys)
            hair_steps.append(key_length)
            for step_index in range(0, key_length):
                if step_index > 0:
                    E.append((len(V)-1, len(V)))
                V.append(hair.hair_keys[step_index].co_object(obj_eval, modifier_eval, hair_eval))
        return V, E

    def to_VEs(obj_eval, modifier_eval, system, system_eval):
        V ,E = [], []
        hair_steps = []
        for hair_index in range(0, len(system.particles)):
            hair = system.particles[hair_index]
            hair_eval = system_eval.particles[hair_index]
            hair_steps.append(len(hair.hair_keys))
            for step_index in range(0, len(hair.hair_keys)):
                if step_index > 0:
                    E.append((len(V)-1, len(V)))
                V.append(hair.hair_keys[step_index].co_object(obj_eval, modifier_eval, hair_eval))
        return V, E, hair_steps

    def to_mesh(depsgraph, obj, select_stems=True):
        po = ParticleOps
        pasy, pamo = po.particle_modifier(obj)
        src_obj_eval, pamo_eval, pasy_eval = oo.evaluated(depsgraph, obj, pamo.name, True)
        dst_obj, dst_mesh = mo.new_mesh(pasy.name, obj.matrix_world)
        V,E,stems = po.to_VEs(src_obj_eval, pamo_eval, pasy, pasy_eval)
        mo.update_VEF(dst_mesh, V, E)
        if select_stems: 
            mo.deselect_Vs(dst_obj)
            mo.select_stems(dst_obj, stems)
        return dst_obj, dst_mesh