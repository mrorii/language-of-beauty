#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import gzip
from tokenizer import NgramTokenizer


META = ('brand', 'maker')
PRICE_REGEX = re.compile(ur'([\d,]+)円')
NGRAM_TOKENIZER = NgramTokenizer()
INVALID_DESCRIPTION_SNIPPET = u'商品情報はメーカー様にご協力いただき掲載しております'
# Remove electronics products as their price range are too different
# from other types of products
INVALID_CATEGORIES = set([
    u'美容グッズ・美容家電 > スキンケアグッズ > スキンケア美容家電',
    u'美容グッズ・美容家電 > ボディグッズ > ボディケア美容家電',
    u'美容グッズ・美容家電 > ヘアグッズ > ヘアケア美容家電',
])


class FeatureVector(dict):
    def todict(self):
        def kv():
            for fname, fval in self.iteritems():
                yield u':'.join(fname), fval
        return dict(kv())


def gzip_or_text(filename):
    if filename.endswith('.gz'):
        return gzip.open(filename)
    return open(filename)


def extract_price(s):
    match = PRICE_REGEX.search(s)
    if match:
        return int(match.groups()[0].replace(',', ''))
    else:
        return None


def is_valid_product(product):
    if 'price' not in product or not product['price']:
        return False

    price = extract_price(product['price'])
    if not price:
        return False
    product['price'] = price

    if 'description' not in product or not product['description']:
        return False

    description = u' '.join(product['description'])
    if INVALID_DESCRIPTION_SNIPPET in description:
        return False

    if ('categories' in product and
            INVALID_CATEGORIES.intersection(product['categories'])):
        return False

    # TODO: remove food (e.g. 'サプリメント・フード')

    return True


def description(product):
    for sentence in product['description']:
        tokens = NGRAM_TOKENIZER.tokenize(sentence)
        for n, w in tokens:
            yield u'desc', str(n), w


def name(product):
    tokens = NGRAM_TOKENIZER.tokenize(product['name'])
    for n, w in tokens:
        yield u'name', str(n), w


def extract(filename):
    with gzip_or_text(filename) as f:
        for line in f:
            product = json.loads(line)

            if not is_valid_product(product):
                continue

            features = FeatureVector()
            for category in product['categories']:
                features[u'meta', u'category', category] = 1
            for meta in META:
                if meta in product and product[meta]:
                    features[u'meta', meta, product[meta]] = 1

            for feat in description(product):
                features[feat] = 1

            for feat in name(product):
                features[feat] = 1

            yield features, product['price']
