#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import itertools
import logging
import os

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Ridge
import numpy

import features


def mae(y_pred, y_truth):
    return numpy.average(numpy.abs(y_pred - y_truth))
    # return numpy.average(numpy.abs(numpy.exp(y_pred) - numpy.exp(y_truth)))


def read_dataset(filename):
    X, y = [], []
    points = features.extract(filename)
    for f, v in points:
        X.append(f.todict())
        y.append(v)
    return X, y


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description='Run regression experiments')
    parser.add_argument('prefix', help='Directory which contains '
                                       '{train|dev|test}.json')
    args = parser.parse_args()

    vectorizer = DictVectorizer()

    logging.info('Loading training data...')
    X_train, y_train = read_dataset(os.path.join(args.prefix, 'train.json'))
    X_train = vectorizer.fit_transform(X_train)
    # y_train = numpy.log(y_train)

    logging.info('Loading development data...')
    X_dev, y_dev = read_dataset(os.path.join(args.prefix, 'dev.json'))
    X_dev = vectorizer.transform(X_dev)
    # y_dev = numpy.log(y_dev)

    logging.info('Training...')
    errors = []
    for penalty in (100, 10, 1, 0.1, 0.01):
        model = Ridge(alpha=penalty)
        print('Penalty: {0}'.format(penalty))
        model.fit(X_train, y_train)
        error = mae(model.predict(X_dev), y_dev)
        errors.append((error, penalty, model))
        print('Dev MAE: {0}'.format(error))

    best_error, best_penalty, best_model = min(errors)

    print('Loading test data...')
    X_test, y_test = read_dataset(os.path.join(args.prefix, 'test.json'))
    X_test = vectorizer.transform(X_test)
    # y_test = numpy.log(y_test)

    print('Tuned penalty: {} (MAE={})'.format(best_penalty, best_error))
    print('Test MAE: {0}'.format(mae(best_model.predict(X_test), y_test)))

    def print_weights(heading, iterator):
        print(heading)
        for i, (feat, weight) in enumerate(iterator):
            print('{0:.4f}\t{1}'.format(weight, feat.encode('utf8')))

    weights = vectorizer.inverse_transform(best_model.coef_)[0]
    sorted_weights = sorted(weights.iteritems(), key=lambda x: x[1],
                            reverse=True)
    print_weights('Most positive 500 weights',
                  itertools.islice(sorted_weights, 500))
    print_weights('Most negative 500 weights',
                  itertools.islice(reversed(sorted_weights), 500))

if __name__ == '__main__':
    main()
