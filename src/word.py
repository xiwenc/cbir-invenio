import cv2


class Word:

    def __init__(self, keypoint, descriptor, value=None, distance=None):
        self.pt = keypoint.pt
        self.size = keypoint.size
        self.angle = keypoint.angle
        self.response = keypoint.response
        self.octave = keypoint.octave
        self.class_id = keypoint.class_id

        self.descriptor = descriptor
        self.value = value
        self.noise = False
        self.distance = distance

    def get_keypoint(self):
        return cv2.KeyPoint(x=self.pt[0], y=self.pt[1], _size=self.size,
                            _angle=self.angle, _response=self.response,
                            _octave=self.octave, _class_id=self.class_id)

    def set_value(self, val):
        self.value = val

    def set_noise(self, value=True):
        self.noise = value

    def __repr__(self):
        return '%s((%d, %d), word=%r)' % (
            self.__class__, self.pt[0], self.pt[1],  self.value
        )

    def export(self):
        return int(self.value)
