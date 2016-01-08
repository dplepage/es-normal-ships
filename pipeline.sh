name=`basename "$1" .blend`;
blender -b "$1" -P r_flat.py -o flat#.png -f 1 > /dev/null;
blender -b "$1" -P r_emit.py -o emit#.png -f 1 > /dev/null;
blender -b "$1" -P r_norm.py -o norm#.png -f 1 > /dev/null;
mkdir -p "outputs/$name";
echo "Rendering $name..."
mv flat1.png "outputs/$name/flat.png";
mv emit1.png "outputs/$name/emit.png";
mv norm1.png "outputs/$name/norm.png";
echo "Generating spin animation..."
python render.py \
    "outputs/$name/flat.png" "outputs/$name/norm.png" "outputs/$name/emit.png" \
    -o "outputs/$name/spin.gif"
