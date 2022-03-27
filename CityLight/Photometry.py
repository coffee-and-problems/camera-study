# This module allows us to use LINQ syntaxis to operate the collections
from py_linq import Enumerable
from astropy.io import fits
import numpy as np
import os
import matplotlib.pyplot as plt
import math
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
        return magnitudes.avg(lambda x: x)

class Standart(object):
    def __init__(self, coords, magnitude, aperture_radius, inner_annulus_radius, outer_annulus_radius):
        self.aperture = CircularAperture(coords, r=aperture_radius)
        self.annulus = CircularAnnulus(coords, r_in=inner_annulus_radius, r_out=outer_annulus_radius)
        self.magnitude = magnitude