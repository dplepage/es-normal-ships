#!/usr/bin/env python
'''
This adds two new GIMP commands, both under Tools/Endless Sky.

The first is "Load Flat Image", which autocrops the image to the size of the
last layer and then loads a flat image as a penultimate layer. If the file is
foo/bar.xcf, it'll load foo/bar.png as the new layer.

Once you've done this, you'll need to manually remove (or edit) any shading
layers etc.

Then, run the second one, "Export Ship", which will export the image as e.g.
foo/bar-flat.png, which is the filename pipeline.py expects to install.

'''

from gimpfu import *
import os.path as pth

def part_one(img, layer):
    name = img.name[:-4]
    png = pth.join(pth.dirname(img.filename), name+".png")
    pdb.plug_in_autocrop(img, img.layers[-1])
    layer = pdb.gimp_file_load_layer(img, png)
    img.add_layer(layer, len(img.layers)-1)

def part_two(img, layer):
    name = img.name[:-4]
    # output = pth.join(pth.dirname(img.filename), '../new-images', name+".png")
    output = img.filename.replace(".xcf", "-flat.png")
    new_image = pdb.gimp_image_duplicate(img)
    layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
    pdb.gimp_file_save(new_image, layer, output, name+".png")
    pdb.gimp_image_delete(new_image)

register(
    "python_fu_es_part_one",
    "Load a flat image",
    "Autocrop the image and load the flat image",
    "Dan Lepage",
    "Dan Lepage",
    "2017",
    "Load Flat Image",
    "*",
    [
        (PF_IMAGE, "img", "Input image", None),
        (PF_DRAWABLE, "layer", "Input layer", None),
    ],
    [],
    part_one, menu="<Image>/Tools/Endless Sky")

register(
    "python_fu_es_part_two",
    "Export a ship",
    "Longer description of doing stuff",
    "Dan Lepage",
    "Dan Lepage",
    "2017",
    "Export Ship",
    "*",
    [
        (PF_IMAGE, "img", "Input image", None),
        (PF_DRAWABLE, "layer", "Input layer", None),
    ],
    [],
    part_two, menu="<Image>/Tools/Endless Sky")

main()
