#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from collections import defaultdict


age_groupings = (
    ("< 20",       lambda age: age < 20),
    ("Early 20's", lambda age: 20 <= age < 25),
    ("Late 20's",  lambda age: 25 <= age < 30),
    ("Early 30's", lambda age: 30 <= age < 35),
    ("Late 30's",  lambda age: 35 <= age < 40),
    ("40's",       lambda age: 40 <= age < 45),
    (">= 50's",    lambda age: age >= 50),
)


def main():
    counts = defaultdict(int)

    for line in sys.stdin:
        user = json.loads(line)
        if 'age' not in user:
            continue

        age = user['age']
        for age_group, func in age_groupings:
            if func(age):
                counts[age_group] += 1

    print '"age_group","count"'
    for age_group, _ in age_groupings:
        count = counts[age_group]
        print '"{0}","{1}"'.format(age_group, count)

if __name__ == '__main__':
    main()
