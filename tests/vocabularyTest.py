import sys
import os
import cv2

sys.path.append('src/')
from album import Album
from utils import clean_dir, recall_and_precision
from logger import logger
from similarity import SimpleCounting

gamma = 0.2


def test():
    album = Album(directory='tests/images')

    build_dir = os.path.join('build', "tests/vocabulary")

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    clean_dir(build_dir)

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    for image in album.images:
        logger.debug('Started processing output for %s' % image.filename)
        grayed = image.grayed
        height, width = grayed.shape
        outfile = os.path.join(build_dir, os.path.basename(image.filename))

        for word in image.words:
            if word.noise:
                logger.debug('Skipped noisy word %d' % word.value)
                continue
            cv2.putText(
                grayed,
                '%d' % word.value,
                (int(word.pt[0]), int(word.pt[1])),
                font, 0.5, (255, 0, 0), 1, cv2.CV_AA)
        cv2.imwrite(outfile, grayed)
        logger.debug('Finished processing output for %s' % image.filename)

    recall_and_precision(album.images, SimpleCounting.distance)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        gamma = float(sys.argv[1])
    test()
