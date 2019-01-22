import logging
import os, sys
from gensim import corpora, models, utils
from gensim.models.wrappers import LdaMallet
import pickle
import argparse

#logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)


def iter_documents(wiki_dir):
    """Iterate over Wiki documents, yielding one document at a time."""
    for fname in os.listdir(wiki_dir):
        # read each document as one big string
        document = open(os.path.join(wiki_dir, fname)).read()
        # parse document into a list of utf8 tokens
        yield utils.simple_preprocess(document)


def iter_lines(data_file):
    new_corpus = open(data_file, 'r')
    for each_line in new_corpus.readlines():
        yield utils.simple_preprocess(each_line.split("|")[0])


class ProbabilityCorpus(object):
    def __init__(self, data_file):
        self.data_file = data_file
        self.dictionary = corpora.Dictionary(iter_lines(data_file))
        # self.dictionary.filter_extremes()  # remove stopwords etc

    def __iter__(self):
        for tokens in iter_lines(self.data_file):
            yield self.dictionary.doc2bow(tokens)

class WikiCorpus(object):
    def __init__(self, wiki_dir):
        self.wiki_dir = wiki_dir
        self.dictionary = corpora.Dictionary(iter_documents(wiki_dir))
        # self.dictionary.filter_extremes()  # remove stopwords etc

    def __iter__(self):
        for tokens in iter_documents(self.wiki_dir):
            yield self.dictionary.doc2bow(tokens)

#model = LdaMallet.load("url_data.model")
#corpus = pickle.load(open("url_data.corpus", "rb"))

model = LdaMallet.load("lda_model")
corpus = pickle.load(open("corpus.prob", "rb"))

print(model)

print(corpus.dictionary)

probability_file = open("probabilities.csv", 'r')
for each_line in probability_file.readlines():
    print(each_line)
    bow = corpus.dictionary.doc2bow(utils.simple_preprocess(each_line.split("|")[0]))
    print(model[bow])
    break
