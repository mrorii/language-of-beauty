#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MeCab

from collections import deque
from neologd import normalize_neologd


def is_number(s):
    """
    Given an arbitrary object, checks if it can be cast to a number.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False

class Tokenizer(object):
    def __init__(self, convert_to_base_form=True, normalize_number=True, append_pos=False):
        self.tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        self.convert_to_base_form = convert_to_base_form
        self.normalize_number = normalize_number
        self.append_pos = append_pos

    def tokenize(self, text):
        # normalized_text = normalize_text(text)
        normalized_text = normalize_neologd(text)
        encoded_text = normalized_text.encode('utf8')
        node = self.tagger.parseToNode(encoded_text)
        node = node.next
        while node.next:
            features = node.feature.split(',')
            base_form = features[-3]
            if self.convert_to_base_form and base_form != '*':
                token = base_form
            else:
                token = node.surface

            token = token.strip()
            if token:
                if self.normalize_number and is_number(token):
                    token = '<NUMBER>'
                if self.append_pos:
                    pos = features[0]
                    token = '{0}-{1}'.format(token, pos)
                yield token.decode('utf8')

            node = node.next

class NgramTokenizer(object):
    def __init__(self, convert_to_base_form=False, normalize_number=True, append_pos=False):
        self.tokenizer = Tokenizer(convert_to_base_form=convert_to_base_form,
                                   normalize_number=normalize_number,
                                   append_pos=append_pos)

    def tokenize(self, text):
        ngram = deque(maxlen = 3)
        tokens = self.tokenizer.tokenize(text)
        for token in tokens:
            ngram.append(token)
            yield (1, token)
            if len(ngram) >= 2:
                yield (2, u'{0} {1}'.format(ngram[-2], ngram[-1]))
            if len(ngram) == 3:
                yield (3, u' '.join(ngram))

if __name__ == '__main__':
    tok = Tokenizer(convert_to_base_form=False)
    tokens = tok.tokenize(u'ﾊﾟｽﾀもﾋﾟｻﾞも食べられない事は無いが、自腹だったら許せないレベルである。')
    for token in tokens:
        print token.encode('utf8')

    ngram_tok = NgramTokenizer()
    tokens = ngram_tok.tokenize(u'ﾊﾟｽﾀもﾋﾟｻﾞも食べられない事は無いが、自腹だったら許せないレベルである。')

    for n, token in tokens:
        print n, token.encode('utf8')
