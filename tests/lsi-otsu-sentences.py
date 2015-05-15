import sys

sys.path.append('src/')
from album import Album
from segmentation import seg_otsu_watershed
from utils import recall_and_precision
from indexing import CorporaOfSentences, LSI

gamma = 0.2


def test():
    album = Album(directory='tests/images', segment_method=seg_otsu_watershed)

    corpora = CorporaOfSentences(album)
    lsi = LSI(corpora.get_corpus(), album.vocabulary.get_size())
    recall_and_precision(album.images, None, indexer=lsi, corpora=corpora)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        gamma = float(sys.argv[1])
    test()
