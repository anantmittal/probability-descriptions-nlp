# set up logging so we see what's going on
import logging
import os, sys
from gensim import corpora, models, utils
from gensim.models.wrappers import LdaMallet
import pickle
import argparse

logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)


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


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input", help="Input file",
                           type=str, default="data.csv", required=False)
    argparser.add_argument("--stage", help="Do you want to 'train' or 'test'?",
                           type=str, default="train", required=True)
    argparser.add_argument("--model_name", help="Model name?",
                           type=str, default="lda_model", required=True)
    argparser.add_argument("--topic_file", help="Where we write results",
                           type=str, default="result", required=False)
    argparser.add_argument("--corpus_file", help="Corpus file name",
                           type=str, default="corpus.prob", required=False)
    argparser.add_argument("--test_string", help="What's the topic of this string?",
                           type=str, default="What are the chances of dying?", required=False)
    args = argparser.parse_args()

    if args.stage == "train":
        if args.input:
            corpus = ProbabilityCorpus(args.input)
            mallet_path = '~/Mallet/bin/mallet'
            model = LdaMallet(mallet_path, corpus, num_topics=5, id2word=corpus.dictionary, workers=4, iterations=1000)
            model.save(args.model_name)
            pickle.dump(corpus, open(args.corpus_file, "wb"))
        else:
            print("Please tell me the --input file?")
            exit()

    elif args.stage == "test":
        model = LdaMallet.load(args.model_name)
        corpus = pickle.load(open(args.corpus_file, "rb"))
        if args.test_string:
            doc = args.test_string
            bow = corpus.dictionary.doc2bow(utils.simple_preprocess(doc))
            print(model[bow])
        else:
            print("Please mention the --test_string?")
            exit()


    if args.topic_file:
        handle = open(args.topic_file, "+w")
        output_str = ""

        topics_as_list_of_weight_word_pairs = model.show_topics(num_topics=-1, num_words=100, log=False,
                                                                formatted=False)
        for topic in topics_as_list_of_weight_word_pairs:
            output_str += "------------------------\n"
            output_str += "TOPIC " + str(topic[0]) + "\n"
            output_str += "------------------------\n"
            for pairs in topic[1]:
                output_str += str(pairs[0]) + " " + str(pairs[1]) + "\n"

        handle.write(output_str)

