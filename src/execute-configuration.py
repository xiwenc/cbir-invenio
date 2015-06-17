import sys

sys.path.append('src/')
from album import Album
from segmentation import seg_slic, seg_otsu_watershed, seg_canny_watershed
from utils import recall_and_precision_ukbench, recall_and_precision_mirflickr
from indexing import CorporaOfSentences, LSI, TFIDF, CorporaOfImages
from similarity import SentenceDiff


def test():
    training_directory = dataset + "-training"
    album = Album(directory=dataset,
                  feature_method=feature_method,
                  clustering_method=clustering_method,
                  segment_method=segment_method,
                  vocabulary_size=vocabulary_size,
                  noise_ratio=noise_ratio,
                  max_samples=10000,
                  training_directory=training_directory
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
    else:
        corpora = None
        indexer = None

    for i in range(3, 400, 4):
        target_image = album.images[i]
        if 'ukbench' in dataset:
            if corpora and indexer:
                recall, precision, results = recall_and_precision_ukbench(
                    target_image, album.images, None, indexer=indexer,
                    corpora=corpora)
            else:
                recall, precision, results = recall_and_precision_ukbench(
                    target_image, album.images, SentenceDiff.distance)
        elif 'mirflickr' in dataset:
            if corpora and indexer:
                recall, precision, results = recall_and_precision_mirflickr(
                    target_image, album.images, None, indexer=indexer,
                    corpora=corpora)
            else:
                recall, precision, results = recall_and_precision_mirflickr(
                    target_image, album.images, SentenceDiff.distance)
        else:
            raise Exception('Unsupported dataset')

        print '{fname}\t{recall}\t{precision}'.format(
            fname=target_image.filename, recall=recall,
            precision=precision)

        for k, v in results:
            print "# {fname}\t{value}".format(fname=k, value=v)

if __name__ == "__main__":
    print ' '.join(sys.argv)
    dataset = sys.argv[1]
    feature_method = sys.argv[2]
    clustering_method = sys.argv[3]
    segment_method = sys.argv[4]
    if segment_method == 'slic':
        segment_method = seg_slic
    elif segment_method == 'canny':
        segment_method = seg_canny_watershed
    elif segment_method == 'otsu':
        segment_method = seg_otsu_watershed
    else:
        segment_method = None
    similarity_method = sys.argv[5]
    corpus_mode = sys.argv[6]
    vocabulary_size = int(sys.argv[7])
    noise_ratio = float(sys.argv[8])

    test()
