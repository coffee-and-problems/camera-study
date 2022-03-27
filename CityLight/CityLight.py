# This module allows us to use LINQ syntaxis to operate the collections
from py_linq import Enumerable
from astropy.io import fits
import numpy as np
import os
import matplotlib.pyplot as plt
from Sort import *
from Photometry import *
from lib import alipylocal as alipy
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry


#Sort().sort_by_camera_and_filter(fits_dir)

standarts = {
    'MicroLine_ML4710_528_513' : {
        'I' : [
        Standart((208.5,220), 10.92, 5.7, 6., 9.),
        Standart((275.5,175), 11.79, 4.9, 5.2, 8.2),
        Standart((282,221), 12.85, 3.7, 4., 7.),
        Standart((279,276), 12.97, 3.7, 4., 7.)
        ],
        'R' : [
        Standart((208.5,220), 11.12, 5.7, 6., 9.),
        Standart((275.5,175), 12.06, 4.9, 5.2, 8.2),
        Standart((282,221), 13.18, 3.7, 4., 7.),
        Standart((279,276), 13.26, 3.7, 4., 7.)
        ]
        },
    'SBIG_ST-7_382_255' : {
        'I' : [
        Standart((223,142), 10.92, 3.2, 3.5, 5.5),
        Standart((182,185.5), 11.79, 2.8, 3.0, 5.0),
        Standart((170,153), 12.85, 2.4, 2.6, 5.6),
        Standart((111,103), 12.97, 2.2, 2.4, 5.4)
        ],
        'R' : [
        Standart((223,142), 11.12, 3.2, 3.5, 5.5),
        Standart((182,185.5), 12.06, 2.8, 3.0, 5.0),
        Standart((170,153), 13.18, 2.4, 2.6, 5.6),
        Standart((111,103), 13.26, 2.2, 2.4, 5.4)
        ]
        }
    }

def make_cat(path):
        cat = alipy.imgcat.ImgCat(path)
        cat.makecat(rerun=False, keepcat=False, verbose=True)
        cat.makestarlist(verbose=False)
        return cat

def find_transform(fits_path, ref_cat):
    cat = make_cat(fits_path)
    idn = alipy.ident.Identification(cat, ref_cat)
    idn.findtrans(verbose=False)
    if idn.ok:
        return idn.trans
    return None


fits_dir = 'data/MicroLine_ML4710_528_513/I'
ref = make_cat('data/test_big/s50716_i_0.fits')
with open(f'CityLight.csv', 'a') as output:
    for subdir, dirs, files in os.walk(fits_dir):
        for f in files:
            with fits.open(os.path.join(subdir, f)) as hdul:
                flat = hdul[0].data - 1000
                transform = find_transform(os.path.join(subdir, f), ref)
                if transform is None:
                    continue
                aligned_standarts = []
                for standart in standarts['MicroLine_ML4710_528_513']['I']:
                    aligned_standarts.append(Standart( transform.apply(standart.x, standart.y), standart.magnitude, standart.aperture_radius, standart.inner_annulus_radius, standart.outer_annulus_radius) )
                avg_background = Photometry.get_avg_background_magnitude(flat, (6,6), aligned_standarts)
                date = hdul[0].header['DATE']
                output.write(f'{f},{date},{avg_background}\n')


fits_dir = 'data/MicroLine_ML4710_528_513/R'
ref = make_cat('data/test_big/s50716_r_12.fits')
with open(f'CityLight.csv', 'a') as output:
    for subdir, dirs, files in os.walk(fits_dir):
        for f in files:
            with fits.open(os.path.join(subdir, f)) as hdul:
                flat = hdul[0].data - 1000
                transform = find_transform(os.path.join(subdir, f), ref)
                if transform is None:
                    continue
                aligned_standarts = []
                for standart in standarts['MicroLine_ML4710_528_513']['R']:
                    aligned_standarts.append(Standart( transform.apply(standart.x, standart.y), standart.magnitude, standart.aperture_radius, standart.inner_annulus_radius, standart.outer_annulus_radius) )
                avg_background = Photometry.get_avg_background_magnitude(flat, (6,6), aligned_standarts)
                date = hdul[0].header['DATE']
                output.write(f'{f},{date},{avg_background}\n')

fits_dir = 'data/SBIG_ST-7_382_255/I'
ref = make_cat('data/test_small/s50716_i_3.fits')
with open(f'CityLight.csv', 'a') as output:
    for subdir, dirs, files in os.walk(fits_dir):
        for f in files:
            with fits.open(os.path.join(subdir, f)) as hdul:
                flat = hdul[0].data - 1000
                transform = find_transform(os.path.join(subdir, f), ref)
                if transform is None:
                    continue
                aligned_standarts = []
                for standart in standarts['MicroLine_ML4710_528_513']['I']:
                    aligned_standarts.append(Standart( transform.apply(standart.x, standart.y), standart.magnitude, standart.aperture_radius, standart.inner_annulus_radius, standart.outer_annulus_radius) )
                avg_background = Photometry.get_avg_background_magnitude(flat, (6,6), aligned_standarts)
                date = hdul[0].header['DATE']
                output.write(f'{f},{date},{avg_background}\n')

fits_dir = 'data/SBIG_ST-7_382_255/R'
ref = make_cat('data/test_small/s50716_r_3.fits')
with open(f'CityLight.csv', 'a') as output:
    for subdir, dirs, files in os.walk(fits_dir):
        for f in files:
            with fits.open(os.path.join(subdir, f)) as hdul:
                flat = hdul[0].data - 1000
                transform = find_transform(os.path.join(subdir, f), ref)
                if transform is None:
                    continue
                aligned_standarts = []
                for standart in standarts['MicroLine_ML4710_528_513']['R']:
                    aligned_standarts.append(Standart( transform.apply(standart.x, standart.y), standart.magnitude, standart.aperture_radius, standart.inner_annulus_radius, standart.outer_annulus_radius) )
                avg_background = Photometry.get_avg_background_magnitude(flat, (6,6), aligned_standarts)
                date = hdul[0].header['DATE']
                output.write(f'{f},{date},{avg_background}\n')
