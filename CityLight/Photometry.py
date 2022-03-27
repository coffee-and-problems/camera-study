# This module allows us to use LINQ syntaxis to operate the collections
from py_linq import Enumerable
from astropy.io import fits
import numpy as np
import os
import matplotlib.pyplot as plt
import math
from numpy.random import default_rng
rng = default_rng(seed = 22)
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry

class Photometry(object):
    def __get_magnitude_in_flux_unit__(data, standart):
        apers = [standart.aperture, standart.annulus]
        phot_table = aperture_photometry(data, apers)
        bkg_mean = phot_table['aperture_sum_1'] / standart.annulus.area
        bkg_sum = bkg_mean * standart.aperture.area
        flux = phot_table['aperture_sum_0'] - bkg_sum
        return 2.5 * math.log(flux, 10) + standart.magnitude

    def get_magnitude_in_flux_unit(data, standarts):
        magnitudes = Enumerable()
        for standatr in standarts:
            magnitudes.append(Photometry.__get_magnitude_in_flux_unit__(data, standatr))
        return magnitudes.avg()

    def get_arcsec_in_pix(data, fov):
        return data.shape[0]/fov[0]

    def get_random_pixels(data, number_of_pixels):
        pixls = []
        for i in range(number_of_pixels):
            coords = (rng.integers(0, data.shape[0]-1), rng.integers(0, data.shape[1]-1))
            pixls.append(data[coords[0], coords[1]])
        return pixls

    def get_avg_background_flux(data):
        background = Photometry.get_random_pixels(data, 200)
        data = Enumerable(data)
        median = data.select_many().median()
        background = Enumerable(background)
        return background.where(lambda x: x < median).avg()

    def get_avg_background_magnitude(data, fov, standarts):
        magnitude_in_flux_unit = Photometry.get_magnitude_in_flux_unit(data, standarts)
        arcsec_in_pix = Photometry.get_arcsec_in_pix(data, fov)
        background = Photometry.get_avg_background_flux(data)
        return magnitude_in_flux_unit - 2.5 * math.log(background/arcsec_in_pix, 10)

class Standart(object):
    def __init__(self, coords, magnitude, aperture_radius, inner_annulus_radius, outer_annulus_radius):
        self.aperture = CircularAperture(coords, r=aperture_radius)
        self.annulus = CircularAnnulus(coords, r_in=inner_annulus_radius, r_out=outer_annulus_radius)
        self.magnitude = magnitude