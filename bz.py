import bpy
import math
import mathutils

def look_at(obj_camera, point):
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = point - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()
#keyframe ;linear

#keyInterp = bpy.context.user_preferences.edit.keyframe_new_interpolation_type
area = bpy.context.area.type
bpy.context.area.type = 'USER_PREFRENCES'
bpy.context.user_preferences.edit.keyframe_new_interpolation_type ='LINEAR'
bpy.context.area.type = area

labels = ["sc", "fcc", "bcc","hex","rhom","st","bct","so","baseco","bco","fco","sm","basecm","tric"]
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

#setup camer
obj_camera = bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(5,5, 3), rotation=(1.26227, 0.0211747, -0.423152))
obj_camera = bpy.context.selected_objects[0] ####<--Fix

look_at(obj_camera, mathutils.Vector((0.0,0.0,0.0)))

sun = bpy.ops.object.light_add(type='SUN', location=(-2, 6, 5))
sun = bpy.context.selected_objects[0] ####<--Fix
sun.data.energy = 3
look_at(sun, mathutils.Vector((0.0,0.0,0.0)))
#setup scene
time = 3*24
scene = bpy.data.scenes["Scene"]
scene.camera = obj_camera
scene.frame_start = 0
scene.frame_end = len(labels)*time

plane = bpy.ops.mesh.primitive_plane_add(size=10000, enter_editmode=False, location=(0, 0, -1.6))

plane = bpy.context.selected_objects[0] ####<--Fix

mat = bpy.data.materials.new(name="plane") #set new material to variable
#ibz_object.active_material.diffuse_color = #change color
mat.diffuse_color = (1,1,1, 1)

plane.data.materials.append(mat)


i = 0
for label in labels[0:3]:
    bz_loc = '/home/john/3D/blender/objs/%s.obj' %(label)
    ibz_loc = '/home/john/3D/blender/objs/%s_r.obj' %(label)
    bz_object = bpy.ops.import_scene.obj(filepath=bz_loc)
    bz_object = bpy.context.selected_objects[0] ####<--Fix
    print('Imported name: ', bz_object.name)

    mod = bz_object.modifiers.new(name = 'wire',type='WIREFRAME')
    mod.thickness = 0.025


    ibz_object = bpy.ops.import_scene.obj(filepath=ibz_loc)
    ibz_object = bpy.context.selected_objects[0] ####<--Fix

    mat = bpy.data.materials.new(name="ibz") #set new material to variable
    mat2 = bpy.data.materials.new(name="bz") #set new material to variable
    #ibz_object.active_material.diffuse_color = #change color
    mat.diffuse_color = (0.133748, 0.0146844, 0.288296, 1)
    mat2.diffuse_color =  (0.0290996, 0.0290996, 0.0290996, 1)
    ibz_object.data.materials[0] = mat
    bz_object.data.materials[0] = mat2


    ibz_object.rotation_mode = 'XYZ'

    bz_object.hide_render=True
    bz_object.keyframe_insert(data_path="hide_render", frame=-1)
    ibz_object.hide_render=True
    ibz_object.keyframe_insert(data_path="hide_render", frame=-1)

    bz_object.hide_render=False
    bz_object.keyframe_insert(data_path="hide_render", frame=i*time)
    ibz_object.hide_render=False
    ibz_object.keyframe_insert(data_path="hide_render", frame=i*time)
    bz_object.hide_render=True
    bz_object.keyframe_insert(data_path="hide_render", frame=i*time+time)
    ibz_object.hide_render=True
    ibz_object.keyframe_insert(data_path="hide_render", frame=i*time+time)

    ibz_object.rotation_euler = (0, 0, 0)
    kf = ibz_object.keyframe_insert('rotation_euler', index=2 ,frame=i*time)
    #kf.interpolation= 'LINEAR'
    bz_object.rotation_euler = (0, 0, 0)
    kf = bz_object.keyframe_insert('rotation_euler', index=2 ,frame=i*time)
    #kf.interpolation= 'LINEAR'

    ibz_object.rotation_euler = (0, 0, math.radians(180))
    kf = ibz_object.keyframe_insert('rotation_euler', index=2 ,frame=i*time + time+1)
    #kf.interpolation= 'LINEAR'
    bz_object.rotation_euler = (0, 0, math.radians(180))
    kf = bz_object.keyframe_insert('rotation_euler', index=2 ,frame=i*time + time + 1)
    #kf.interpolation= 'LINEAR'
    i+=1
