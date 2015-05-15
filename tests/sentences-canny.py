import sys

sys.path.append('src/')
from album import Album
from segmentation import seg_canny_watershed
from utils import recall_and_precision
from similarity import SentenceDiff

gamma = 0.2


def test():
    album = Album(directory='tests/images', segment_method=seg_canny_watershed)
    recall_and_precision(album.images, SentenceDiff.distance)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        gamma = float(sys.argv[1])
    test()
