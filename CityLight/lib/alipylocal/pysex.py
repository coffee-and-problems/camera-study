"""
Author: Nicolas Cantale - n.cantale@gmail.com

Small module wrapping sextractor. The idea is to have a single function taking an image
and returning a sextractor catalog.

Dependencies:
 - sextractor (mandatory)
 - astroasciidata (mandatory)
 - numpy (optional, needed for the array support)
 - pyfits (optional, needed for the array support)


Usage:

    import pysex
    cat = pysex.run(myimage, params=['X_IMAGE', 'Y_IMAGE', 'FLUX_APER'], conf_args={'PHOT_APERTURES':5})
    print cat['FLUX_APER']

"""

from math import hypot
import os
import shutil
from os import path
import subprocess
from lib import asciidatalocal as asciidata
from numpy import genfromtxt, argsort


def _get_cmd(img, img_ref, conf_args):
    ref = img_ref if img_ref is not None else ''
    pathToFile = path.join("lib", "alipysex.sex")
    if os.name == "nt":  # we are on MS Windows now
        pathToSex = path.join("lib", "sex.exe")
    else:
        pathToSex = 'sex'
    cmd = ' '.join([pathToSex, ref, img, '-c %s ' % pathToFile])
    args = [''.join(['-', key, ' ', str(conf_args[key])]) for key in conf_args]
    cmd += ' '.join(args)
    return cmd


def _read_cat(path_to_file='alipysex.cat'):
    if path.exists(path_to_file):
        return asciidata.open(path_to_file)
    else:
        return None


def _cleanup():
    files = [f for f in os.listdir('.') if 'alipysex.' in f]
    for f in files:
        os.remove(f)
        if path.exists('alipysex.cat'):
            os.remove('alipysex.cat')


def filterPolCat(catInName, catOutName, polarFilterName, camera):
    matchDist = 2.0
    polarFilterName = polarFilterName.lower()
    polarFilterIdx = camera.polar_filters.index(polarFilterName)
    shift_dx = camera.polar_pair_shift[polarFilterIdx][0]
    shift_dy = camera.polar_pair_shift[polarFilterIdx][1]

    cat = genfromtxt(catInName)
    # Sort catalogue by x-coordinate
    try:
        cat = cat[argsort(cat[:, 1])]
    except IndexError:
        # empty cat
        return None
    pairs = []

    for i, obj in enumerate(cat):
        xObj = obj[1]
        yObj = obj[2]
        xPair = xObj + shift_dx
        yPair = yObj + shift_dy
        minDist = 1e5

        for obj2 in cat[i:]:
            x2 = obj2[1]
            y2 = obj2[2]
            if x2 > xPair + 5:
                # Pair object can not be so far away from the original one
                break
            dist = hypot(x2-xPair, y2-yPair)
            if dist < minDist:
                minDist = dist
                pairObj = obj2
        if minDist < matchDist:
            # possible pair object found
            pairs.append((obj, pairObj))

    fout = open(catOutName, "w")
    fout.truncate(0)
    for line in open(catInName):
        if line.startswith("#"):
            fout.write(line)
    for objNum, pair in enumerate(pairs):
        outStr = " ".join([str(v) for v in pair[0][1:]])
        fout.write("%i %s\n" % (objNum+1, outStr))
    fout.close()


def run(image='', imageref='', params=[], conf_file=None, conf_args={}, keepcat=True,
        rerun=False, catdir=None, polarMode=None, camera=None):
    """
    Run sextractor on the given image with the given parameters.

    image: filename or numpy array
    imageref: optional, filename or numpy array of the the reference image
    params: list of catalog's parameters to be returned
    conf_file: optional, filename of the sextractor catalog to be used
    conf_args: optional, list of arguments to be passed to sextractor (overrides the parameters in the conf file)


    keepcat : should I keep the sex cats ?
    rerun : should I rerun sex even when a cat is already present ?
    catdir : where to put the cats (default : next to the images)


    Returns an asciidata catalog containing the sextractor output

    Usage exemple:
        import pysex
        cat = pysex.run(myimage, params=['X_IMAGE', 'Y_IMAGE', 'FLUX_APER'], conf_args={'PHOT_APERTURES':5})
        print cat['FLUX_APER']
    """

    # Preparing permanent catalog filepath :
    (imgdir, filename) = path.split(image)
    (common, ext) = path.splitext(filename)
    possibleCatName = path.join(imgdir, "%s.cat" % (common))
    if path.exists(possibleCatName):
        # there is prepared catalogue
        cat = _read_cat(possibleCatName)
        return cat

    catfilename = common + "alipysexcat"  # Does not get deleted by _cleanup(), even if in working dir !
    if keepcat:
        if catdir:
            if not path.isdir(catdir):
                os.makedirs(catdir)

    if catdir:
        catpath = path.join(catdir, catfilename)
    else:
        catpath = path.join(imgdir, catfilename)

    # Checking if permanent catalog already exists :
    if rerun is False and isinstance(image, str):
        if path.exists(catpath):
            cat = _read_cat(catpath)
            return cat

    # Otherwise we run sex :
    if polarMode is None:
        conf_args['CATALOG_NAME'] = 'alipysex.cat'
    else:
        conf_args['CATALOG_NAME'] = 'alipysex_polar.cat'
    conf_args['PARAMETERS_NAME'] = path.join('lib', 'alipysex.param')
    _cleanup()
    if not isinstance(image, str):
        try:
            import pyfits
        except ImportError:
            from astropy.io import fits as pyfits
        im_name = 'alipysex.fits'
        pyfits.writeto(im_name, image.transpose())
    else:
        im_name = image
    if not isinstance(imageref, str):
        try:
            import pyfits
        except ImportError:
            from astropy.io import fits as pyfits

        imref_name = 'alipysex.ref.fits'
        pyfits.writeto(imref_name, imageref.transpose())
    else:
        imref_name = imageref
    cmd = _get_cmd(im_name, imref_name, conf_args)
    res = subprocess.call(cmd, shell=True)
    if res:
        print("Error during sextractor execution!")
        _cleanup()
        return

    # Clean polar data if necessary
    if polarMode is not None:
        filterPolCat("alipysex_polar.cat", "alipysex.cat", polarMode, camera)
    # Keeping the cat at a permanent location :
    if keepcat and isinstance(image, str):
        shutil.copy('alipysex.cat', catpath)

    # Returning the cat :
    cat = _read_cat()
    # _cleanup()
    return cat
