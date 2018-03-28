# set up logging so we see what's going on
import logging
import os
from gensim import corpora, models, utils
from gensim.models.wrappers import LdaMallet

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)


def iter_documents(wiki_dir):
    """Iterate over Wiki documents, yielding one document at a time."""
    for fname in os.listdir(wiki_dir):
        # read each document as one big string
        document = open(os.path.join(wiki_dir, fname)).read()
        # parse document into a list of utf8 tokens
        yield utils.simple_preprocess(document)


class WikiCorpus(object):
    def __init__(self, wiki_dir):
        self.wiki_dir = wiki_dir
        self.dictionary = corpora.Dictionary(iter_documents(wiki_dir))
        # self.dictionary.filter_extremes()  # remove stopwords etc

    def __iter__(self):
        for tokens in iter_documents(self.wiki_dir):
            yield self.dictionary.doc2bow(tokens)


# set up the streamed corpus
corpus = WikiCorpus('./xpdopen/')

mallet_path = '~/Mallet/bin/mallet'
model = LdaMallet(mallet_path, corpus, num_topics=5, id2word=corpus.dictionary, workers=4, iterations=1000)

handle = open("mallet_topics.txt", "+w")
output_str = ""

topics_as_list_of_weight_word_pairs = model.show_topics(num_topics=5, num_words=100, log=False, formatted=False)
for topic in topics_as_list_of_weight_word_pairs:
    output_str += "------------------------\n"
    output_str += "TOPIC " + str(topic[0]) + "\n"
    output_str += "------------------------\n"
    for pairs in topic[1]:
        output_str += str(pairs[0]) + " " + str(pairs[1]) + "\n"

handle.write(output_str)
