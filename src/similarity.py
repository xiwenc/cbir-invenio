import numpy
import difflib


class SimpleCounting(object):

    @staticmethod
    def distance(image1, image2):
        counts1 = SimpleCounting.count(image1)
        counts2 = SimpleCounting.count(image2)

        similar_min = reduce(
            lambda x, y: x + y,
            map(min, zip(counts1, counts2))
        )
        similar_max = reduce(
            lambda x, y: x + y,
            map(max, zip(counts1, counts2))
        )
        if similar_max == 0:
            return float("inf")
        else:
            return float(similar_min) / similar_max

    @staticmethod
    def count(image):
        counts = numpy.zeros(image.vocabulary_size)
        for word in image.words:
            counts[word.value] = counts[word.value] + 1
        return counts


class SentenceDiff(object):

    @staticmethod
    def distance(image1, image2):
        assert len(image1.sentences) > 0
        assert len(image2.sentences) > 0

        ratios = []
        for s in image1.sentences:
            ratios.append(max(map(
                lambda x: SentenceDiff.distance_sentence(s, x),
                image2.sentences
            )))

        ratio_total = sum(ratios)
        count = len(ratios)
        return ratio_total / float(count)

    @staticmethod
    def distance_sentence(sentence1, sentence2):
        sm = difflib.SequenceMatcher(
            None,
            [word.value for word in sentence1.words],
            [word.value for word in sentence2.words],
            autojunk=False
        )
        return sm.ratio()
