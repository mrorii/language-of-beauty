#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os

from gensim import corpora

from tokenizer import Tokenizer

def parse_args():
    description = '''
    Builds a dictionary from reviews
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('prefix')
    return parser.parse_args()


def load_reviews(filename):
    tokeniser = Tokenizer(normalize_number=False)
    with open(filename, 'r') as f:
        for line in f:
            review = json.loads(line)
            nested_tokens = [tokeniser.tokenize(sentence)
                             for sentence in review['text']]
            tokens = [token for sublist in nested_tokens for token in sublist]
            yield tokens


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                        level=logging.INFO)

    args = parse_args()
    reviews = load_reviews(os.path.join(args.prefix, 'review.json'))

    dictionary = corpora.Dictionary(reviews)
    dictionary.save(os.path.join(args.prefix, 'review.dict'))

if __name__ == '__main__':
    main()
