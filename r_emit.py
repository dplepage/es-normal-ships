'''
blender -b <blend file> -P r_emit.py -f 1 -o emit#.png

Renders the given file without any lights named 'Sun' or 'Lamp'. Use other
names for emission lights. The above would save to emit1.png
'''

import bpy
import sys

s = bpy.context.scene

# Remove the sun, which is occasionally called Lamp or Lamp.001
for obj in s.objects:
    if obj.type == 'LAMP':
        if obj.name.startswith("Sun") or obj.name.startswith("Lamp"):
            s.objects.unlink(obj)
