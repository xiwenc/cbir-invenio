import operator
import gzip
import pickle

from logger import logger
from utils import recursive_list_dir, distribute
from image import Image
from vocabulary import Kmeans, Som, BoW


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
                 do_distribute=False, vocabulary=None, filenames=None):
        self.images = []
        self.vocabulary = None
        self.directory = directory
        self.feature_method = feature_method
        self.clustering_method = clustering_method
        self.max_samples = max_samples
        self.do_distribute = do_distribute
        self.segment_method = segment_method

        if vocabulary is not None:
            self.vocabulary = vocabulary
            self.feature_method = vocabulary.get_feature_method()

        if len(self.images) <= 0:
            self.images = self.import_images(directory=directory, filenames=filenames)

        if self.vocabulary is None:
            self.vocabulary = self.compute_vocabulary(vocabulary_size,
                                                      self.images,
                                                      method=clustering_method)
            self.images = self.compute_words(self.images)
            self.compute_noisy_words(gamma=noise_ratio)
        else:
            self.images = self.compute_words(self.images)
        self.images = self.set_noisy_words(self.images)
        self.images = self.compute_segments(self.images, self.segment_method)

    def compute_segments(self, images, segment_method):
        logger.debug('Started compute_segments')
        if segment_method is not None:
            if self.do_distribute and False:
                images = distribute(worker_f_compute_sentences,
                                    segment_method,
                                    images)
            else:
                images = [image.compute_sentences(segment_method) for image in images]
        else:
            logger.warn("No segment_method: Skipping sentences mapping")
        logger.debug('Completed compute_segments')
        return images

    def create_test_images(self, directory=None, filenames=None):
        logger.debug('Started create_test_images')
        testimages = self.import_images(directory=directory, filenames=filenames)
        testimages = self.compute_words(testimages)
        testimages = self.set_noisy_words(testimages)
        testimages = self.compute_segments(testimages, self.segment_method)
        logger.debug('Completed create_test_images')
        return testimages

    def import_images(self, directory=None, filenames=None):
        logger.debug('Started import_images')
        if directory is not None:
            filenames = recursive_list_dir(directory)
        else:
            filenames = filenames
        images = [
            Image(fn) for fn in filenames
        ]
        if self.do_distribute:
            images = distribute(worker_f_compute_raw_words,
                                self.feature_method,
                                self.images)
        else:
            images = [image.compute_raw_words(self.feature_method) for image in images]

        logger.debug('Completed import_images')
        return images

    def compute_vocabulary(self, size, images, method='kmeans'):
        logger.debug('Started compute_vocabulary')
        assert len(images) > 0

        vocabulary = Album.get_clustering(method)
        vocabulary.set_feature_method(self.feature_method)

        data = []
        for image in images:
            for word in image.words:
                data.append(word.descriptor)
        vocabulary.train(data, size,
                         max_samples=self.max_samples)
        logger.debug('Completed compute_vocabulary')
        return vocabulary

    def compute_words(self, images):
        assert len(images) > 0
        assert self.vocabulary is not None
        logger.debug('Started compute_words')
        images = distribute(worker_f_compute_words, self.vocabulary, images)
        images = sorted(images, key=lambda x: x.filename)
        logger.debug('Completed compute_words')
        return images

    @staticmethod
    def get_clustering(method):
        if method == 'kmeans':
            return Kmeans()
        elif method == 'som':
            return Som()
        elif method == 'none':
            return BoW()
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

        logger.debug('Low frequency words count: %d', noisy_words_count)
        for k, v in counts_sorted[:noisy_words_count]:
            ratio = v / float(total)
            logger.debug('%d is low frequency word, %d (%r) occurences' % (
                k,
                v,
                ratio
            ))
            self.vocabulary.add_noise(k)

        logger.debug('Completed compute_noisy_words')

    def set_noisy_words(self, images):
        logger.debug('Started set_noisy_words')
        for idx in self.vocabulary.noise:
            self._set_noise(idx, images)
        logger.debug('Completed set_noisy_words')
        return images

    def _set_noise(self, idx, images):
        for image in images:
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
