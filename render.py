'''
Helper for rendering animated gifs of spinning ships.

Basic usage:

render.py flat.png norm.png emit.png -o spin.gif

This will combine a flat image, a normal map, and an emission map to render
the flat image under a circle of different lighting conditions, and then
rotate and merge those images into an animated gif.

Run render.py -h for more advanced options, not all of which are tested.
'''
from PIL import Image
import numpy as np
import sys
import tempfile, contextlib

def load(fname, size=(800, 800)):
    img = Image.open(fname)
    img.thumbnail(size, Image.ANTIALIAS)
    data = np.array(list(img.getdata()), np.uint8)
    data = data.reshape(img.width, img.height, data.shape[-1])
    return data/255.0

def coords(img, xspan=(-1,1), yspan=(-1,1)):
    w,h,_ = img.shape
    x = np.linspace(xspan[0], xspan[1], w)
    y = np.linspace(yspan[0], yspan[1], h)
    xx,yy = np.meshgrid(x,y)
    return np.dstack([xx,yy,np.zeros((w,h))])

def normalize(img):
    w,h,_ = img.shape
    return img/(np.sum(img*img, 2)**.5).reshape(w,h,1)

def scale(lpos, pos, norm):
    lightvecs = lpos - pos
    lightdirs = normalize(lightvecs)
    dots = np.clip(np.sum(lightdirs*norm, 2), 0, 1)
    return dots.reshape(*dots.shape, 1)

def render(lpos, pos, norm, flat, emit):
    result = np.clip(scale(lpos, pos, norm)*flat + emit, 0, 1)
    return np.dstack([result, alpha])

def angles(n):
    return np.linspace(0, np.pi*2, n+1)[:-1]

def imgize(img):
    return Image.fromarray(np.uint8(img*255))

def deg(theta):
    return theta*180.0/np.pi

def dim(s):
    bits = s.split('x')
    if len(bits) == 1:
        return (int(bits), int(bits))
    return (int(bits[0]), int(bits[1]))

@contextlib.contextmanager
def gettmp(name=None):
    if name is not None:
        if not os.path.exists(name):
            os.makedirs(name, exist_ok=True)
        yield name
    else:
        with tempfile.TemporaryDirectory() as tdir:
            yield tdir

if __name__ == '__main__':
    import argparse
    import os, os.path
    import subprocess as sp

    parser = argparse.ArgumentParser('render.py')
    parser.add_argument('flat', action='store')
    parser.add_argument('norm', action='store')
    parser.add_argument('emit', action='store', default=None)
    parser.add_argument('--size', '-s', default=(400,400), action='store', type=dim)
    parser.add_argument('--frames', '-n', default=120, action='store', type=int)
    parser.add_argument('--transparent', '-t', default=False, action='store_true')
    parser.add_argument('--tdir', '-d', default=None, action='store')
    parser.add_argument('--outfile', '-o', default='anim.gif', action='store')
    args = parser.parse_args()
    size = args.size
    flat = load(args.flat, args.size)
    alpha = flat[..., 3].reshape(*args.size, 1)
    flat = flat[..., :3]
    raw_norm = load(args.norm, size)
    # Unpack normals and renormalize them just to be safe
    norm = normalize(raw_norm[...,:3]*2-1)
    emit = load(args.emit, size)[...,:3] if args.emit else 0
    pos = coords(flat)

    if not args.transparent:
        # fill transparent regions with blackness
        emit *= alpha
        flat *= alpha
        alpha[:] = 1

    procs = []
    with gettmp(args.tdir) as tdir:
        for i, theta in enumerate(angles(args.frames)):
            sys.stdout.write('\r{:03}/{:03}'.format(i+1, args.frames))
            sys.stdout.flush()
            lpos = [4*np.sin(-theta), 4*np.cos(-theta), 3]
            frame = render(lpos, pos, norm, flat, emit)
            suffix = "{:03}.png".format(i)
            fname = os.path.join(tdir, 'frame'+suffix)
            tname = os.path.join(tdir, 'lit'+suffix)
            imgize(frame).save(tname)
            procs.append(sp.Popen([
                'convert', tname, '-alpha', 'set', '(',
                    '+clone',
                    '-background', 'none' if args.transparent else 'black',
                    '-rotate', str(deg(theta)), ')',
                '-gravity', 'center', '-compose', 'Src', '-composite', fname
            ]))
        for proc in procs:
            # Make sure all the converts succeeded
            assert not proc.wait()
        print('\nConverting...')
        os.system('convert -coalesce -delay 3 -loop 0 "{}/frame*.png" "{}"'.format(tdir, args.outfile))

