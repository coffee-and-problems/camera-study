from astropy.io import fits
import numpy as np
import os

fits_dir = 'darks'

for i in range(1,6):
    for j in range(1,6):
        with open(f'T_E_part{i}{j}.csv', 'a') as f:
            for subdir, dirs, files in os.walk(fits_dir):
                for dark in files:
                    with fits.open(os.path.join(subdir, dark)) as hdul:
                        x = hdul[0].data.shape[0]/5
                        y = hdul[0].data.shape[1]/5
                        T = hdul[0].header['CCD-TEMP']
                        data = hdul[0].data[int(x*(i-1)):int(x*i), int(y*(j-1)):int(y*j)]
                        E_int = np.sum(data)
                        f.write(f'{dark},{T},{E_int}\n')