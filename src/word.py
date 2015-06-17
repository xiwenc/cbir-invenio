class Word:

    def __init__(self, keypoint, descriptor, value=None, distance=None):
        self.pt = keypoint.pt

        self.descriptor = descriptor
        self.value = value
        self.noise = False
        self.distance = distance

    def set_value(self, val):
        self.value = val

    def set_noise(self, value=True):
        self.noise = value

    def export(self):
        return int(self.value)
