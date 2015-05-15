from gensim import models, similarities


def document(sequence):
    counts = {}
    for item in sequence:
        if item in counts:
            counts[item] = counts[item] + 1
        else:
            counts[item] = 1

    result = []
    for k, v in counts.iteritems():
        result.append((k, v))
    return result


class LSI(object):
    def __init__(self, corpus, num_features):
        self.lsi = models.LsiModel(corpus, num_topics=num_features)
        self.index = similarities.SparseMatrixSimilarity(
            self.lsi[corpus],
            num_features=num_features
        )

    def similarity(self, doc):
        sims = self.index[self.lsi[doc]]
        return sims


class TFIDF(object):
    def __init__(self, corpus, num_features):
        self.tfidf = models.TfidfModel(corpus)
        self.index = similarities.SparseMatrixSimilarity(
            self.tfidf[corpus],
            num_features=num_features
        )

    def similarity(self, doc):
        sims = self.index[self.tfidf[doc]]
        return sims


class CorporaOfImages(object):
    def __init__(self, album):
        self.album = album
        self.index = []
        self.corpus = []

    def get_corpus(self):
        if len(self.corpus) > 0:
            return self.corpus

        for image in self.album.images:
            sequences = []
            for sentence in image.sentences:
                sequence = sentence.export()
                sequences.extend(sequence)
            doc = document(sequences)
            self.corpus.append(doc)
            self.index.append(image)

        return self.corpus

    def similarity(self, model, image):
        sequences = []
        for sentence in image.sentences:
            sequence = sentence.export()
            sequences.extend(sequence)
        doc = document(sequences)
        sims = model.similarity(doc)

        fitness = {}
        for i, j in list(enumerate(sims)):
            filename = self.index[i].filename
            fitness[filename] = j
        return fitness


class CorporaOfSentences(object):
    def __init__(self, album, min_length=5):
        self.album = album
        self.index = []
        self.corpus = []
        self.min_length = min_length

    def get_corpus(self):
        if len(self.corpus) > 0:
            return self.corpus

        for image in self.album.images:
            for sentence in image.sentences:
                sequence = sentence.export()
                doc = document(sequence)
                if len(sequence) >= self.min_length:
                    self.corpus.append(doc)
                    self.index.append(image)

        return self.corpus

    def similarity(self, model, image):
        result = None
        for sentence in image.sentences:
            sequence = sentence.export()
            doc = document(sequence)
            if len(sequence) >= self.min_length:
                sims = model.similarity(doc)
                if result is None:
                    result = sims
                else:
                    result = [max(i, j) for i, j in zip(result, sims)]

        fitness = {}
        for i, j in list(enumerate(result)):
            filename = self.index[i].filename
            if filename not in fitness:
                fitness[filename] = j
            else:
                fitness[filename] = max(fitness[filename], j)
        return fitness
