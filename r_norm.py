'''
blender -b <blend file> -P r_norm.py -f 1 -o norm#.png

Renders the given file as a normal map. The above would save to norm1.png

Note: This requires normal_tex.jpg to be in the same directory.

'''

import bpy

# Import the normal texture
img = bpy.data.images.load('./normal_tex.jpg')
tex = bpy.data.textures.new('Normals', type = 'IMAGE')
tex.image = img
mat = bpy.data.materials.new('Normals')
mtex = mat.texture_slots.add()
mtex.texture = tex
mtex.texture_coords = 'NORMAL'
mat.use_shadeless = True # ignore lighting

s = bpy.context.scene
# Apply material to all meshes in the scene
for ob in s.objects:
    if ob.type != 'MESH':
        continue
    # Make sure to account for objects w/ 0 materials OR >1 materials
    n = len(ob.data.materials)
    ob.data.materials.clear()
    for i in range(max(n,1)):
        ob.data.materials.append(mat)
