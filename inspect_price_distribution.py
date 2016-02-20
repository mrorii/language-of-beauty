#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os

from common import get_price, get_age_group, load_items


def facet(review, product, user, facet_type):
    facet_type = facet_type.lower()
    if facet_type == 'none':
        return 'all'
    elif facet_type == 'age':
        return get_age_group(user, review)
    else:
        raise ValueError('Invalid facet type')


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description='Inspect price distributions')
    parser.add_argument('prefix', help='Directory containing json files')
    parser.add_argument('facet', help='Facet', choices=['age', 'none'])
    args = parser.parse_args()

    logging.info('Loading products...')
    product_by_id = load_items(os.path.join(args.prefix, 'product.json'),
                               'product_id')
    logging.info('Loading users...')
    user_by_id = load_items(os.path.join(args.prefix, 'user.json'),
                            'user_id')

    print '"facet","price"'
    with open(os.path.join(args.prefix, 'review.json')) as f:
        for line in f:
            review = json.loads(line)
            product = product_by_id[review['product_id']]
            price = get_price(product)
            if not price:
                continue

            user = user_by_id[review['user_id']]
            fct = facet(review, product, user, args.facet)
            if not fct:
                continue

            print '"{0}","{1}"'.format(fct, price)

if __name__ == '__main__':
    main()
