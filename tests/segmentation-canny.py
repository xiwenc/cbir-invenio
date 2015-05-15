import sys
import os
import cv2

sys.path.append('src/')
from segmentation import seg_canny_watershed
from utils import clean_dir, recursive_list_dir
from logger import logger


def test():
    build_dir = os.path.join('build', "tests/segmentation-canny")

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    clean_dir(build_dir)
    images = recursive_list_dir('tests/images')

    for image in images:
        logger.info('Processing %s' % image)
        original = cv2.imread(image)
        outfile = os.path.join(build_dir, os.path.basename(image))
        cv2.imwrite(outfile, original)

        (_, markers, count) = seg_canny_watershed(original)
        cv2.imwrite(outfile.replace('.jpg', '-segments.jpg'), markers)
        logger.info('{filename} has {segments} segments'.format(
            filename=image,
            segments=count
        ))

if __name__ == "__main__":
    test()
