from astropy.io import fits
import os
import shutil

class Sort(object):
    def sort_by_camera_and_filter(self, fits_dir):
        for subdir, dirs, files in os.walk(fits_dir):
            for fit in files:
                fit_path = os.path.join(subdir, fit)
                with fits.open(fit_path) as hdul:
                    camera_dir = self._get_camera_dir_(hdul)
                    filter_dir = self._get_filter_dir_(fit)
                    self._create_if_not_exist_(os.path.join(fits_dir, camera_dir))
                    self._create_if_not_exist_(os.path.join(fits_dir, camera_dir, filter_dir))
                shutil.move(fit_path, os.path.join(fits_dir, camera_dir, filter_dir))

    def _get_camera_dir_(self, hdul):
        instrument_name = hdul[0].header['INSTRUME'].replace(" ", "_")
        return f"{instrument_name}_{hdul[0].header['NAXIS1']}_{hdul[0].header['NAXIS2']}"

    def _get_filter_dir_(self, file_name):
        return file_name.split('_')[1].upper()

    def _create_if_not_exist_(self, path):
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)