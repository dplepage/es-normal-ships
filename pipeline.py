import sys
from pathlib import Path
from subprocess import check_call, DEVNULL
from PIL import Image

shipdir = Path('../endless-sky/images/ship/')

def blender(source, args, *more_args):
    app = '/Applications/blender.app/Contents/MacOS/blender'
    args = [app, '-b', str(source)] + args.split()+list(more_args)
    return check_call(args, stdout=DEVNULL)

def convert(source, dest, args, *more_args):
    args = args.split()+list(more_args)
    args = ['convert', str(source)] + args + [str(dest)]
    return check_call(args)

def stem(path):
    return path.stem.replace("-bump", "").replace("-flat", "")

def render(source):
    '''Given a blend file, create flat and normal images from it

    Given foo/bar.blend, the outputs will be foo/bar.png and foo/bar-bump.png.

    Assuming foo/bar.xcf exists, you should then launch it and run the two tools
    from ./gimp-plugin.

    TODO Replace 'bump' with 'norm'. They're normal maps, not bump maps.
    '''
    name = stem(source)
    print("Rendering '{}'".format(name))
    blender(source.parent/'{}.blend'.format(name), '-P r_flat.py -o flat#.png -f 1')
    blender(source.parent/'{}.blend'.format(name), '-P r_norm.py -o bump#.png -f 1')
    convert('flat1.png', source.parent/'{}.png'.format(name), '-trim +repage')
    convert('bump1.png', source.parent/'{}-bump.png'.format(name), '-trim +repage')

def install(source):
    '''Install images and cleanup.

    The input should be e.g. foo/bar.blend; this script assumes that
    foo/bar.png, foo/bar-flat.png, foo/bar-bump.png, foo/bar.blend, and
    foo/bar.xcf all exists.

    bar-flat.png and bar-bump.png will be resized, transparently padded, and
    moved to ../endless-sky/images/ship/; all of the files named above will then
    be moved to ./done/
    '''
    name = stem(source)
    workspace = source.parent
    complete = Path("./done")
    names = {x:name+y for (x,y) in dict(
        bump='-bump.png',
        flat='-flat.png',
        plain='.png',
        blend='.blend',
        xcf='.xcf'
    ).items()}
    dest = shipdir/names['plain']
    if not dest.exists():
        print("No existing ship: '{}'".format(name))
        return
    bump = workspace/names['bump']
    flat = workspace/names['flat']
    if not bump.exists() or not flat.exists():
        print("No rendering for ship: '{}'".format(name))
        return
    print("Installing '{}'".format(name))
    # Read the right size from the existing image
    w, h = Image.open(str(dest)).size
    # Resize to 4px smaller and add a 2x2 transparent border
    args = '-resize {}x{} -bordercolor transparent -border 2x2'.format(w-4,h-4)
    convert(workspace/names['flat'], dest, args)
    # Ditto the bump
    convert(bump, shipdir/names['bump'], args)
    # Cleanup
    for _, name in names.items():
        (workspace/name).rename(complete/name)


if __name__ == '__main__':
    cmd = globals()[sys.argv[1]]
    for blend in sys.argv[2:]:
        cmd(Path(blend))
