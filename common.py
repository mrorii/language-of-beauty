#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re

PRICE_REGEX = re.compile(ur'([\d,]+)円')


def convert_to_utf8(json_obj):
    '''
    Converts simple json python representations to utf-8 recursively.

    Refer to:
    - http://stackoverflow.com/a/13105359
    - http://stackoverflow.com/q/18337407
    '''
    if isinstance(json_obj, dict):
        return dict((convert_to_utf8(key), convert_to_utf8(value))
                    for key, value in json_obj.iteritems())
    elif isinstance(json_obj, list):
        return [convert_to_utf8(element) for element in json_obj]
    elif isinstance(json_obj, unicode):
        return json_obj.encode('utf-8')
    else:
        return json_obj


def json_dumps_utf8(json_obj):
    input_utf8 = convert_to_utf8(json_obj)
    # seperators argument ensures no spaces between fields
    # in json (allowing for a more compact representation)
    return json.dumps(input_utf8, ensure_ascii=False,
                      encoding='utf-8', separators=(',', ':'))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_price(product):
    if 'price' not in product:
        return None

    price = product['price']
    match = PRICE_REGEX.search(price)
    if match:
        return int(match.groups()[0].replace(',', ''))
    else:
        return None


def get_age(user):
    if not user or not 'age' in user or not user['age']:
        return
    return user['age']

def get_age_group(user):
    age = get_age(user)
    if not age:
        return

    if age < 20:
        return '< 20'
    elif 20 <= age < 25:
        return "Early 20's"
    elif 25 <= age < 30:
        return "Late 20's"
    elif 30 <= age < 35:
        return "Early 30's"
    elif 35 < age < 40:
        return "Late 30's"
    elif 40 <= age < 50:
        return "40's"
    else:
        return ">= 50's"
