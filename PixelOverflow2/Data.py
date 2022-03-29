class Data(object):
    def __init__(self, exposure, intensity):
        self.exposure = exposure
        self.intensity = intensity

    def get_exposure_and_intensity(self, coords):
        return (self.exposure, self.intensity[ coords[0], coords[1] ])