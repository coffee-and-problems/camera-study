# This module allows us to use LINQ syntaxis to operate the collections
from py_linq import Enumerable
from astropy.io import fits
import numpy as np
import os
from Sort import *

fits_dir = 'data'

Sort().sort_by_camera_and_filter(fits_dir)