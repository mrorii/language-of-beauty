#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os

from gensim import corpora
from gensim.models.ldamulticore import LdaMulticore

from common import SimpleTokenizer


def parse_args():
    description = '''
    Finds topics from reviews
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('prefix')
    parser.add_argument('--no_below', type=int, default=5)
    parser.add_argument('--no_above', type=float, default=0.95)
    parser.add_argument('--num_topics', type=int, default=64)
    parser.add_argument('--workers')
    return parser.parse_args()


class ReviewCorpus(object):
    def __init__(self, filename, dictionary):
        self.filename = filename
        self.dictionary = dictionary
        self.tokenizer = SimpleTokenizer()

    def __iter__(self):
        with open(self.filename) as f:
            for line in f:
                review = json.loads(line)
                tokens = self.tokenizer.tokenize(review)
                yield self.dictionary.doc2bow(tokens)


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    args = parse_args()

    dictionary = corpora.Dictionary.load(os.path.join(args.prefix, 'review.dict'))
    logging.info('Pruning dictionary')
    dictionary.filter_extremes(no_below=args.no_below,
                               no_above=args.no_above)

    corpus = ReviewCorpus(os.path.join(args.prefix, 'review.json'),
                          dictionary)

    logging.info('Computing LDA model')
    lda = LdaMulticore(corpus, num_topics=args.num_topics, id2word=dictionary,
                       workers=args.workers)

    logging.info('Persisting LDA model')
    lda.save(os.path.join(args.prefix, 'review.ldamodel'))

if __name__ == '__main__':
    main()
