import bpy

bpy.ops.object.add(type='MESH', enter_editmode=False, location=(0,0,0))
o = bpy.context.object
o.name = 'myobject'
o.data.from_pydata([(0,0,0),(1,0,0),(0,1,0),(0,0,1)],[],[(0,1,2),(0,1,3),(1,2,3),(0,2,3)])
o.data.update()
