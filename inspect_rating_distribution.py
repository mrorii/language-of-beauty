#!/usr/bin/env python

import sys
import json
from collections import defaultdict

from common import is_number


def main():
    counts = defaultdict(int)

    for line in sys.stdin:
        review = json.loads(line)
        if 'rating' not in review:
            continue
        rating = review['rating']

        if not is_number(rating):
            continue

        counts[rating] += 1

    print '"rating","count"'
    for rating, count in counts.iteritems():
        print '"{0}","{1}"'.format(rating, count)

if __name__ == '__main__':
    main()
