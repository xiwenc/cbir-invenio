import cv2

from logger import logger
from word import Word
import sentence


class Image(object):

    def __init__(self, source):
        if isinstance(source, str):
            logger.info('Initializing: %s', source)
            self.filename = source
            self.raw = cv2.imread(self.filename)
        else:
            logger.info('Initializing: %s %s',
                        source['filename'], source['suffix']
                        )
            self.filename = '%s_%s' % (
                            source['filename'], source['suffix']
            )
            self.raw = source['fragment']
        self.grayed = cv2.cvtColor(self.raw, cv2.COLOR_BGR2GRAY)
        self.sentences = []
        self.words = []
        self.vocabulary_size = 0

    def compute_raw_words(self, engine):
        logger.debug('Started computing raw words for %s' % self.filename)
        keypoints, descriptors = Image.detect_and_compute(
            self.grayed, engine
        )
        for i in range(len(keypoints)):
            self.words.append(Word(keypoints[i], descriptors[i]))
        logger.debug('Finished computing raw words for %s' % self.filename)
        return self

    def compute_words_values(self, vocabulary):
        map(
            lambda x: x.set_value(vocabulary.winner(x.descriptor)),
            self.words
        )
        self.vocabulary_size = vocabulary.get_size()
        return self

    @staticmethod
    def detect_and_compute(image, engine='surf', hesian=400):
        if engine == 'sift':
            _sift = cv2.SIFT()
            return _sift.detectAndCompute(image, None)
        elif engine == 'surf':
            _surf = cv2.SURF(hesian)
            return _surf.detectAndCompute(image, None)
        else:
            raise Exception('Unsupported engine type: %s' % engine)

    def compute_sentences(self, segment_function):
        (segments, markers, count) = segment_function(self.raw)

        for segment in segments:
            s = sentence.Sentence()
            s.compute(self.grayed, segment, self.words)
            if len(s.words) <= 0:
                logger.info('Discarded segment ({x}, {y}): '
                            'not enough words'.format(
                                x=s.x,
                                y=s.y
                            ))
            else:
                self.sentences.append(s)

        self.sentences = sorted(self.sentences, key=lambda z: (z.x, z.y))
        if len(self.sentences) <= 0:
            logger.warning('No sentences found in {fname}'.format(
                fname=self.filename
            ))
        # assert len(self.sentences) > 0
        return self

    def export(self):
        return {
            'filename': self.filename,
            'sentences': self.deflate(),
        }

    def deflate(self):
        sep = u'. '
        return sep.join([segment.deflate() for segment in self.segments])
