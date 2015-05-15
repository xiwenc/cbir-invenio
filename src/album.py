import operator
import os
import gzip
import pickle

from logger import logger
from utils import recursive_list_dir, distribute
from image import Image
from vocabulary import Kmeans, Som


default_filename = 'album.pickle.gz'


def worker_f_compute_words(vocabulary, targets, queue):
    result = []
    for target in targets:
        result.append(target.compute_words_values(vocabulary))
    queue.put(result)


def worker_f_compute_raw_words(feature_method, targets, queue):
    result = []
    for target in targets:
        result.append(target.compute_raw_words(feature_method))
    queue.put(result)


def worker_f_compute_sentences(segment_method, targets, queue):
    result = []
    for target in targets:
        result.append(target.compute_sentences(segment_method))
    queue.put(result)


class Album(object):

    def __init__(self, directory='.', vocabulary_size=1000,
                 feature_method='surf', clustering_method='kmeans',
                 segment_method=None, noise_ratio=0.2, max_samples=0,
                 do_distribute=False):
        self.images = []
        self.vocabulary = None
        self.directory = directory
        self.feature_method = feature_method
        self.clustering_method = clustering_method
        self.max_samples = max_samples
        self.do_distribute = do_distribute

        if os.path.exists(default_filename):
            self.load()
        if len(self.images) <= 0:
            self.import_images()
        if self.vocabulary is None:
            self.compute_vocabulary(vocabulary_size, method=clustering_method)
            self.compute_words()
            self.compute_noisy_words(gamma=noise_ratio)
            if segment_method is not None:
                if self.do_distribute and False:
                    self.images = distribute(worker_f_compute_sentences,
                                             segment_method,
                                             self.images)
                else:
                    self.images = [image.compute_sentences(segment_method) for image in self.images]
            else:
                logger.warn("No segment_method: Skipping sentences mapping")

    def import_images(self):
        logger.debug('Started import_images')
        filenames = recursive_list_dir(self.directory)
        self.images = [
            Image(fn) for fn in filenames
        ]
        if self.do_distribute:
            self.images = distribute(worker_f_compute_raw_words,
                                     self.feature_method,
                                     self.images)
        else:
            self.images = [image.compute_raw_words(self.feature_method) for image in self.images]

        logger.debug('Completed import_images')

    def compute_vocabulary(self, size, method='kmeans'):
        assert len(self.images) > 0
        logger.debug('Started compute_vocabulary')

        self.vocabulary = Album.get_clustering(method)
        if self.vocabulary.get_size() <= 0:
            data = []
            for image in self.images:
                for word in image.words:
                    data.append(word.descriptor)
            self.vocabulary.train(data, size,
                                  max_samples=self.max_samples)
        logger.debug('Completed compute_vocabulary')

    def compute_words(self):
        assert len(self.images) > 0
        assert self.vocabulary is not None
        logger.debug('Started compute_words')
        self.images = distribute(worker_f_compute_words, self.vocabulary,
                                 self.images)
        self.images = sorted(self.images, key=lambda x: x.filename)
        logger.debug('Completed compute_words')

    @staticmethod
    def get_clustering(method):
        if method == 'kmeans':
            return Kmeans()
        elif method == 'som':
            return Som()
        else:
            raise Exception(
                'Unsupported clustering method: {method}'.format(
                    method=method
                ))

    def compute_noisy_words(self, gamma=0.20):
        assert self.vocabulary is not None
        assert len(self.images) > 0
        logger.debug('Started compute_noisy_words')

        size = self.vocabulary.get_size()
        counts = dict()
        for i in range(size):
            counts[i] = 0
        for image in self.images:
            for word in image.words:
                counts[word.value] = counts[word.value] + 1

        counts_sorted = sorted(counts.iteritems(), key=operator.itemgetter(1))
        noisy_words_count = int(gamma * size) / 2
        logger.debug('Stop words count: %d', noisy_words_count)
        total = sum(counts)
        for k, v in counts_sorted[size - noisy_words_count:]:
            ratio = v / float(total)
            logger.debug('%d is stop word, %d (%r) occurences' % (k, v, ratio))
            self._set_noise(k)

        logger.debug('Low frequency words count: %d', noisy_words_count)
        for k, v in counts_sorted[:noisy_words_count]:
            ratio = v / float(total)
            logger.debug('%d is low frequency word, %d (%r) occurences' % (
                k,
                v,
                ratio
            ))
            self._set_noise(k)

        logger.debug('Completed compute_noisy_words')

    def _set_noise(self, idx):
        for image in self.images:
            for word in image.words:
                if idx == word.value:
                    word.set_noise(True)

    def save(self, filename=default_filename):
        with gzip.open(filename, 'wb') as outfile:
            pickle.dump((
                self.vocabulary,
            ), outfile)

    def load(self, filename=default_filename):
        with gzip.open(filename, 'rb') as infile:
            (
                self.vocabulary,
            ) = pickle.load(infile)
