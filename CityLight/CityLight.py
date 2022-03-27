# This module allows us to use LINQ syntaxis to operate the collections
from py_linq import Enumerable
from astropy.io import fits
import numpy as np
import os
import matplotlib.pyplot as plt
from Sort import *
from Photometry import *
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry

fits_dir = 'data/test_big'

#Sort().sort_by_camera_and_filter(fits_dir)

#circle1_big = plt.Circle((208.5,220), 5.7, color='r', fill=False)
#circle2_big = plt.Circle((275.5,175), 4.9, color='r', fill=False)
#circle3_big = plt.Circle((282,221), 3.7, color='r', fill=False)
#circle4_big = plt.Circle((279,276), 3.7, color='r', fill=False)

#circle1_small = plt.Circle((223,142), 3.2, color='r', fill=False)
#circle2_small = plt.Circle((182,185.5), 2.8, color='r', fill=False)
#circle3_small = plt.Circle((170,153), 2.4, color='r', fill=False)
#circle4_small = plt.Circle((111,103), 2.2, color='r', fill=False)

#aperture1_big = CircularAperture((208.5,220), r=5.7); annulus1_big = CircularAnnulus((208.5,220), r_in=6., r_out=9.)


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

for subdir, dirs, files in os.walk(fits_dir):
    for f in files:
        with fits.open(os.path.join(subdir, f)) as hdul:
            flat = hdul[0].data - 1000
            #plt.figure()
            #ax = plt.gca()
            #ax.cla()
            #ax.imshow(flat, cmap='gray', vmin=2000, vmax=20000)
            #plt.title(f)
            ##ax.add_patch(circle1_big)
            ##ax.add_patch(circle2_big)
            ##ax.add_patch(circle3_big)
            ##ax.add_patch(circle4_big)
            #plt.show()

            print(Photometry.get_avg_background_magnitude(flat, (6,6), standarts['MicroLine_ML4710_528_513']['I']))
            


#fits_dir = 'data/test_small'

#for subdir, dirs, files in os.walk(fits_dir):
#    for f in files:
#        with fits.open(os.path.join(subdir, f)) as hdul:
#            matrix_size = (hdul[0].data.shape[0], hdul[0].data.shape[1])
#            flat = hdul[0].data
#            plt.figure()
#            ax = plt.gca()
#            ax.cla()
#            ax.imshow(flat, cmap='gray', vmin=100, vmax=2000)
#            ax.add_patch(circle1_small)
#            ax.add_patch(circle2_small)
#            ax.add_patch(circle3_small)
#            ax.add_patch(circle4_small)
#            plt.show()