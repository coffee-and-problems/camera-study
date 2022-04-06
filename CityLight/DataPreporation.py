# This module allows us to use LINQ syntaxis to operate the collections
from py_linq import Enumerable
from astropy.io import fits
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
        Standart((208.5,220), 10.92, 8, 9, 11),
        Standart((275.5,175), 11.79, 8, 9, 11),
        Standart((282,221), 12.85, 8, 9, 11),
        Standart((279,276), 12.97, 8, 9, 11)
        ],
        'R' : [
        Standart((208.5,220), 11.12, 8, 9, 11),
        Standart((275.5,175), 12.06, 8, 9, 11),
        Standart((282,221), 13.18, 8, 9, 11),
        Standart((279,276), 13.26, 8, 9, 11)
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
        cat.makecat(rerun=False, keepcat=True, verbose=False)
        cat.makestarlist(verbose=False)
        return cat

def find_transform(fits_path, ref_cat):
    cat = make_cat(fits_path)
    idn = alipy.ident.Identification(cat, ref_cat)
    idn.findtrans(verbose=False)
    if idn.ok:
        return idn.trans
    return None

def process_files(dirs, ref, dark, camera_name, pix_scale):
    with open(f'CityLight.csv', 'a', buffering=5) as output:
        for d in dirs:
            for subdir, dirs, files in os.walk(os.path.join(fits_dir, d)):
                for f in files:
                    with fits.open(os.path.join(subdir, f)) as hdul:
                        data = hdul[0].data
                        transform = find_transform(os.path.join(subdir, f), ref)
                        if transform is None:
                            continue
                        aligned_standarts = []
                        for standart in standarts[camera_name][d]:
                            aligned_standarts.append(Standart(transform.apply(standart.x, standart.y), standart.magnitude, standart.aperture_radius, standart.inner_annulus_radius, standart.outer_annulus_radius) )
                        try:
                            avg_background = Photometry.get_avg_background_magnitude(data, pix_scale, aligned_standarts, dark)
                        except:
                            avg_background = 'nan'
                        date = hdul[0].header['DATE-OBS']
                        temp = hdul[0].header['CCD-TEMP']
                        output.write(f'{f},{date},{avg_background},{temp}\n')


with open(f'CityLight.csv', 'w') as output:
    output.write('name,date,background_magnitude,temp\n')

fits_dir = 'data/MicroLine_ML4710_528_513'
dirs = next(os.walk(fits_dir))[1]
ref = make_cat('data/MicroLine_ML4710_528_513/I/s50716_i_0.fits')
with fits.open('dark1S0.FIT') as hdul:
    dark = hdul[0].data * hdul[0].header['EXPTIME'] / 60

process_files(dirs, ref, dark, 'MicroLine_ML4710_528_513', 1.35)

fits_dir = 'data/SBIG_ST-7_382_255'
dirs = next(os.walk(fits_dir))[1]
ref = make_cat('data/SBIG_ST-7_382_255/I/s50716_i_3.fits')
with fits.open('dark_0.fits') as hdul:
    dark = hdul[0].data * hdul[0].header['EXPTIME'] / 60

process_files(dirs, ref, dark, 'SBIG_ST-7_382_255', 1.84)