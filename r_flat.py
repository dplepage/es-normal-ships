'''
blender -b <blend file> -P r_flat.py -f 1 -o flat#.png

Renders the given file without any lights except an ambient enviromental
light. The above would save to flat1.png

'''


import bpy
import sys

s = bpy.context.scene

# Remove all lighting
for obj in s.objects:
    if obj.type == 'LAMP':
        s.objects.unlink(obj)

# Set plain flat environment light
s.world.light_settings.use_environment_light = True
