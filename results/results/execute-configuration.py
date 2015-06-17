import sys

sys.path.append('../src/')
from album import Album
from segmentation import seg_slic, seg_otsu_watershed, seg_canny_watershed
from utils import compute_similarities
from indexing import CorporaOfSentences, LSI, TFIDF, CorporaOfImages
from similarity import SentenceDiff, SimpleCounting


if __name__ == "__main__":
    print(' '.join(sys.argv))
    if len(sys.argv) == 3:
        config = sys.argv[2].split('/')[2].replace('.results', '')
        params = config.split('-')
        segment_method = params[4]
        similarity_method = params[5]
        corpus_mode = params[6]
        feature_method = params[0]
        clustering_method = params[1]
        vocabulary_size = int(params[2])
        noise_ratio = float(params[3].replace('0', '0.'))
    else:
        segment_method = sys.argv[2]
        similarity_method = sys.argv[3]
        corpus_mode = sys.argv[4]
        feature_method = sys.argv[5]
        clustering_method = sys.argv[6]
        vocabulary_size = int(sys.argv[7])
        noise_ratio = float(sys.argv[8])
    dataset = sys.argv[1]
    testdataset = dataset.replace("-training", "-test")

    if segment_method == 'slic':
        segment_method = seg_slic
    elif segment_method == 'canny':
        segment_method = seg_canny_watershed
    elif segment_method == 'otsu':
        segment_method = seg_otsu_watershed
    else:
        segment_method = None

    album = Album(directory=dataset,
                  feature_method=feature_method,
                  clustering_method=clustering_method,
                  segment_method=segment_method,
                  vocabulary_size=vocabulary_size,
                  noise_ratio=noise_ratio,
                  )

    if similarity_method == 'lsi' and corpus_mode == 'segments':
        corpora = CorporaOfSentences(album)
        indexer = LSI(corpora.get_corpus(), album.vocabulary.get_size())
    elif similarity_method == 'lsi' and corpus_mode == 'images':
        corpora = CorporaOfImages(album)
        indexer = LSI(corpora.get_corpus(), album.vocabulary.get_size())
    elif similarity_method == 'tfidf' and corpus_mode == 'segments':
        corpora = CorporaOfSentences(album)
        indexer = TFIDF(corpora.get_corpus(), album.vocabulary.get_size())
    elif similarity_method == 'tfidf' and corpus_mode == 'images':
        corpora = CorporaOfImages(album)
        indexer = TFIDF(corpora.get_corpus(), album.vocabulary.get_size())
    elif similarity_method == 'bow' and corpus_mode == 'images':
        corpora = SimpleCounting.distance
        indexer = None
    elif similarity_method == 'ratcliff' and corpus_mode == 'segments':
        corpora = SentenceDiff.distance
        indexer = None
    else:
        corpora = None
        indexer = None

    testimages = album.create_test_images(directory=testdataset)

    for target_image in testimages:
        if corpora and indexer:
            results = compute_similarities(target_image, album.images, None,
                                           indexer=indexer, corpora=corpora)
        else:
            results = compute_similarities(target_image, album.images,
                                           corpora)

        for k, v in results:
            print("# {target}\t{fname}\t{value}".format(
                target=target_image.filename, fname=k, value=v))
