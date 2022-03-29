from numpy.random import default_rng
rng = default_rng(seed = 22)
import os
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from Data import Data

fits_dir = 'flats'

def get_random_pixel(number_of_pixels):
    coords = []
    for i in range(number_of_pixels):
        coords.append( (rng.integers(0, 500), rng.integers(0, 500)) )
    return coords

def plot_scatter(x, y):
    plt.title(f'Зависимость пикселя с координатами {c} от экспозиции')
    plt.scatter(x, y, s=3)
    plt.savefig(f'Пиксель {c}.png')
    plt.clf()

def take_only_non_negative(x, y):
    x_non_negative = []
    y_non_negative = []
    for (x_i, y_i) in zip(x, y):
        if y_i >= 0:
            x_non_negative.append(x_i)
            y_non_negative.append(y_i)
    return (x_non_negative, y_non_negative)

def plot_scatter_and_fit(x, y):
    (x_non_negative, y_non_negative) = take_only_non_negative(x, y)
    m, b = np.polyfit(x_non_negative, y_non_negative, 1)
    plt.title(f'Зависимость пикселя с координатами {c} от экспозиции')
    plt.scatter(x, y, s=3)
    plt.plot(x, m*x + b, 'm-', linewidth=0.8, label=f'{m:.2f} x + {b:.2f}')
    plt.legend()
    plt.savefig(f'Пиксель {c}_fit.png')
    plt.clf()


plt.figure()
exposure_and_intensities = []
coords = get_random_pixel(16)
for subdir, dirs, files in os.walk(fits_dir):
    for f in files:
        with fits.open(os.path.join(subdir, f)) as hdul:
            matrix_size = (hdul[0].data.shape[0], hdul[0].data.shape[1])
            flat = Data(hdul[0].header['EXPTIME'], hdul[0].data)
            plt.title(f"Экспозиция: {flat.exposure}с")
            plt.imshow(flat.intensity, cmap='gray', vmin=-32000, vmax=32000)
            plt.colorbar()
            idontlikepythonbecauseofthis = f.split('.')[0]
            plt.savefig(f'{idontlikepythonbecauseofthis}.png')
            plt.clf()
            exposure_and_intensity = []
            for c in coords:
                exposure_and_intensity.append(flat.get_exposure_and_intensity(c))
            exposure_and_intensities.append(exposure_and_intensity)

#convert to numpy array to use slices:
exposure_and_intensities = np.array(exposure_and_intensities)

for (j, c) in zip(range(16), coords):
    exposure = exposure_and_intensities[:,j,0]
    intensities = exposure_and_intensities[:,j,1]
    plot_scatter(exposure, intensities)
    plot_scatter_and_fit(exposure, intensities)
