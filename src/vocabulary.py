import cv2
import random
import gzip
import pickle
import numpy

from logger import logger

default_filename = 'vocabulary.pickle.gz'


class VobabularyBase(object):
    """
    Base class
    """

    def __init__(self):
        self.noise = []
        self.feature_method = None

    def save(self, filename=default_filename):
        with gzip.open(filename, 'wb') as outfile:
            pickle.dump(self, outfile)

    @staticmethod
    def load(filename=default_filename):
        with gzip.open(filename, 'rb') as infile:
            return pickle.load(infile)

    def add_noise(self, id):
        self.noise.append(id)

    def is_noise(self, id):
        return id in self.noise

    def set_feature_method(self, feature_method):
        self.feature_method = feature_method

    def get_feature_method(self):
        return self.feature_method


class Kmeans(VobabularyBase):
    def __init__(self):
        VobabularyBase.__init__(self)
        self.clusters = []

    def train(self, data, ksize, max_samples=0, iterations=1000):
        assert len(data) > ksize
        assert iterations > 0

        logger.debug(
            'Started training kmeans with ksize={ksize}'.format(
                ksize=ksize
            ))
        if max_samples > 0:
            assert max_samples >= ksize
            data = random.sample(data, max_samples)

        logger.debug('Training kmeans with {samples} samples'.format(
                     samples=len(data)
                     ))

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                    iterations,
                    1.0)

        ret, _, centers = cv2.kmeans(
            numpy.array(data),
            ksize,
            criteria,
            10,  # attempts
            cv2.KMEANS_PP_CENTERS
        )
        self.clusters = centers
        logger.debug(
            'Completed training kmeans with return={ret}'.format(
                ret=ret
            ))

    def winner(self, sample):
        assert self.get_size() > 0

        best_dist = None
        best_id = None
        for i in range(self.get_size()):
            distance = numpy.linalg.norm(sample - self.clusters[i])
            if best_id is None or distance <= best_dist:
                best_id = i
                best_dist = distance
        return best_id

    def get_size(self):
        return len(self.clusters)


import minisom


class Som(VobabularyBase):
    def __init__(self):
        VobabularyBase.__init__(self)
        self.network = None
        self.x = -1
        self.y = 0

    def train(self, data, ksize, max_samples=0, iterations=1000):
        self.x = 20
        self.y = ksize / self.x
        assert self.get_size() == ksize
        input_len = len(data[0])
        assert input_len > 0

        logger.debug(
            'Started training som with size={x}, {y}'.format(
                x=self.x,
                y=self.y
            ))
        if max_samples > 0:
            data = random.sample(data, max_samples)

        logger.debug('Training SOM with {samples} samples'.format(
                     samples=len(data)
                     ))

        if self.network is None:
            self.network = minisom.MiniSom(self.x, self.y, input_len)

        self.network.train_batch(numpy.array(data), iterations)
        logger.debug('Completed training som')

    def winner(self, sample):
        x, y = self.network.winner(sample)
        best_id = x + y * self.x
        return best_id

    def get_size(self):
        return self.x * self.y


class BoW(VobabularyBase):
    def __init__(self):
        VobabularyBase.__init__(self)
        self.clusters = []

    def train(self, data, ksize, max_samples=0):
        assert len(data) > ksize

        logger.debug(
            'Started BOW vocabulary with ksize={ksize}'.format(
                ksize=ksize
            ))
        if max_samples > 0:
            assert max_samples >= ksize
            data = random.sample(data, max_samples)

        if ksize <= 0:
            self.clusters = data
        else:
            self.clusters = random.sample(data, ksize)

    def winner(self, sample):
        assert self.get_size() > 0

        best_dist = None
        best_id = None
        for i in range(self.get_size()):
            distance = numpy.linalg.norm(sample - self.clusters[i])
            if best_id is None or distance <= best_dist:
                best_id = i
                best_dist = distance
        return best_id

    def get_size(self):
        return len(self.clusters)
