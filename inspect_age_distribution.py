#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from collections import defaultdict

from common import get_age_group


def main():
    counts = defaultdict(int)

    for line in sys.stdin:
        user = json.loads(line)
        age_group = get_age_group(user)
        counts[age_group] += 1

    print '"age_group","count"'
    for age_group, count in counts.iteritems():
        print '"{0}","{1}"'.format(age_group, count)

if __name__ == '__main__':
    main()
