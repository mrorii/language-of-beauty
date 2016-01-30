#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


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
