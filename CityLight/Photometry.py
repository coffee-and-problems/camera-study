# This module allows us to use LINQ syntaxis to operate the collections
from py_linq import Enumerable
import math
import numpy as np
from numpy.random import default_rng
rng = default_rng(seed = 22)
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry, ApertureStats

class Photometry(object):
    def __get_magnitude_in_flux_unit__(data, standart):
        apers = [standart.aperture, standart.annulus]
        phot_table = aperture_photometry(data, apers)
        aperstats = ApertureStats(data, standart.annulus)
        bkg_mean = aperstats.mean
        bkg_sum = bkg_mean * standart.aperture.area
        flux = phot_table['aperture_sum_0'] - bkg_sum
        return 2.5 * math.log(flux, 10) + standart.magnitude

    def get_magnitude_in_flux_unit(data, standarts):
        magnitudes = Enumerable()
        for standatr in standarts:
            magnitudes.append(Photometry.__get_magnitude_in_flux_unit__(data, standatr))
        return magnitudes.avg()

    def get_avg_background_flux(data):
        return np.median(data)

    def get_avg_background_magnitude(data, arcsec_in_pix, standarts, bias=None):
        if bias is not None:
            phot_data = data - bias
        else:
            phot_data = data
        magnitude_in_flux_unit = Photometry.get_magnitude_in_flux_unit(phot_data, standarts)
        background = Photometry.get_avg_background_flux(phot_data)
        F = background/arcsec_in_pix/arcsec_in_pix
        return magnitude_in_flux_unit - 2.5 * math.log(F, 10)


class Standart(object):
    def __init__(self, coords, magnitude, aperture_radius, inner_annulus_radius, outer_annulus_radius):
        self.x = coords[0]
        self.y = coords[1]
        self.magnitude = magnitude
        self.aperture_radius = aperture_radius
        self.inner_annulus_radius = inner_annulus_radius
        self.outer_annulus_radius = outer_annulus_radius
        self.aperture = CircularAperture(coords, r = aperture_radius)
        self.annulus = CircularAnnulus(coords, r_in=inner_annulus_radius, r_out=outer_annulus_radius)