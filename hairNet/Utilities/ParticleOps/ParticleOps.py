import bpy
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
    
    def hair_system(obj, system_name):
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.modifiers.new("HairNet", 'PARTICLE_SYSTEM') #Adding a particle modifier also works but requires pushing/pulling the active object and selection.
        # override = {"object": obj, "particle_system": systemName} #Set up context override
        # bpy.ops.object.particle_system_add(override)
        obj.particle_systems[-1].name = system_name
        obj.particle_systems[-1].settings.type = 'HAIR'
        obj.particle_systems[-1].settings.render_step = 5
        return obj.particle_systems[system_name]