# es-normal-ships
Some experiments with normal-mapping Endless Sky ship images.


Basic usage:
`. pipeline.sh wardragon.blend`


Here are some example results of applying this directly to the blendfiles:

![small](https://cloud.githubusercontent.com/assets/107468/12189699/22092494-b58e-11e5-8b7c-38cd5ea46a0a.gif) ![small](https://cloud.githubusercontent.com/assets/107468/12189709/5796756c-b58e-11e5-8c86-4172b56aa51a.gif) 
![small](https://cloud.githubusercontent.com/assets/107468/12189714/7c6d03d8-b58e-11e5-8820-bd1eae8fd37e.gif) ![small](https://cloud.githubusercontent.com/assets/107468/12189741/b957785a-b58e-11e5-8ceb-264a62afb056.gif)
![small](https://cloud.githubusercontent.com/assets/107468/12189762/f520e448-b58e-11e5-8ff4-35875333bf3d.gif) ![small](https://cloud.githubusercontent.com/assets/107468/12189763/f76911e4-b58e-11e5-87eb-0bd13b571be0.gif)

Here's an example where I used the blender scripts to generate initial images, put the flat-color image through the same GIMP modifications as the ES image, and then used that modified map to generate the spin. Untextured on the left, textured on the right:

![spin](https://cloud.githubusercontent.com/assets/107468/12189541/bd694484-b58c-11e5-951c-64a5d23cee80.gif)
![color](https://cloud.githubusercontent.com/assets/107468/12189556/dba2e554-b58c-11e5-9fdb-b088d48f243b.gif)

This looked something like:
```shell
blender -b "pug maboro.blend" -P r_flat.py -o flat#.png -f 1;
blender -b "pug maboro.blend" -P r_norm.py -o norm#.png -f 1;
blender -b "pug maboro.blend" -P r_emit.py -o emit#.png -f 1;
python render.py flat1.png norm1.png emit1.png -o spin.gif
gimp "pug maboro.xcf" # in gimp, go replace the grayscale image with flat1.png
python render.py flat_tex.png norm1.png emit1.png -o color.gif
```
