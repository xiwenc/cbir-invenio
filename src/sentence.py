import cv2
import numpy

from logger import logger


class Sentence(object):

    def __init__(self):
        self.x = -1
        self.y = -1
        self.words = []
        self.mask = None

    def compute(self, grayed, contour, all_words):
        (self.x, self.y), (_, _), _ = cv2.minAreaRect(contour)
        for word in all_words:
            if cv2.pointPolygonTest(contour, word.pt, False) >= 0:
                if word.noise:
                    logger.warn('Skipping noisy word: {word}'.format(
                        word=word
                    ))
                else:
                    self.words.append(word)
        mask8 = numpy.zeros(grayed.shape, numpy.uint8)
        cv2.drawContours(mask8, [contour], -1, (255, 0, 0), -1)
        mask32 = numpy.int32(mask8)
        self.mask = cv2.convertScaleAbs(mask32)
        self.words = sorted(self.words, key=lambda x: (x.pt[0], x.pt[1]))
        logger.debug('Compute sentence with {count} words: {words}'.format(
            count=len(self.words),
            words=self.export()
        ))

    def __repr__(self):
        return '%s(%d, %r, %r)' % (
            self.__class__,
            len(self.words),
            self.x, self.y
        )

    def export(self):
        return [word.export() for word in self.words]
