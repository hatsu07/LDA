#!/usr/bin/env python

import numpy as np
from gensim import corpora, models
from collections import Counter
import glob
import nlp


def makeCorpus(path):
    with open(path, 'r') as f:
        doc = [nlp.normalize(line) for line in f.readlines()]

    m = nlp.mecab.Mecab()
    words = [morph.stem for line in doc if line for sent in line.split(
        '/') if sent for morph in m.parse(sent) if morph.part == '名詞']

    count = Counter(words)
    doc = [c[0] for c in count.items() if c[1] >= 5]
    return doc


def rmNoise(ds, threshold=0.0001):
    N = len(ds)

    def tfidf(d):
        count = Counter(d)
        n = len(d)

        def tf(w):
            return count[w] / n

        def idf(w):
            return np.log(N / sum([w in doc for doc in ds]))

        return [(word, tf(word) * idf(word)) for word in d]

    return [[item[0] for item in doc if item[1] > threshold]
            for doc in list(map(tfidf, ds))]

paths = glob.glob('../Corpora/*.txt')

docs = list(map(makeCorpus, paths))
exDocs = rmNoise(docs, threshold=0.0001)

dictionary = corpora.Dictionary(exDocs)
corpus = [dictionary.doc2bow(x) for x in exDocs]
lda = models.ldamodel.LdaModel(
    corpus=corpus, num_topics=len(paths), id2word=dictionary)

testText = [['箸', '皿', 'コップ', '茶碗']]
# testText = [['洗面所', '蛇口', '歯ブラシ', 'タオル', 'コップ']]
# testText = [['浴槽', 'シャワー', 'シャンプー', 'タオル']]
# testText = [['シャツ', 'タンス', 'ボタン']]

testCorpus = [dictionary.doc2bow(x) for x in testText]

for item in lda[testCorpus]:
    print(list(map(lambda x: (x[0], str(round(x[1] * 100, 2)) + '%'), item)))
