#!/usr/bin/env python
#  coding=utf-8
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT license.

from nltk.tokenize import TweetTokenizer
import re

re_art = re.compile(r'\b(a|an|the)\b')
re_punc = re.compile(r'[!"#$%&()*+,-./:;<=>?@\[\]\\^`{|}~_\']')


def normalize_answer(s):
    """
    Lower text and remove punctuation, articles and extra whitespace.
    """
    s = s.lower()
    s = re_punc.sub(' ', s)
    s = re_art.sub(' ', s)
    s = ' '.join(s.split())
    return s


def clean_str(txt):
    """
    Lower text, remove url, illegal char, etc.
    """
    txt = txt.lower()
    txt = re.sub('^', ' ', txt)
    txt = re.sub('$', ' ', txt)

    # url and tag
    words = []
    for word in txt.split():
        i = word.find('http')
        if i >= 0:
            word = word[:i] + ' ' + '__url__'
        words.append(word.strip())
    txt = ' '.join(words)

    # remove markdown URL
    txt = re.sub(r'\[([^\]]*)\] \( *__url__ *\)', r'\1', txt)

    # remove illegal char
    txt = re.sub('__url__', 'URL', txt)
    txt = re.sub(r"[^A-Za-z0-9():,.!?\"\']", " ", txt)
    txt = re.sub('URL', '__url__', txt)

    # contraction
    add_space = ["'s", "'m", "'re", "n't", "'ll", "'ve", "'d", "'em"]
    tokenizer = TweetTokenizer(preserve_case=False)
    txt = ' ' + ' '.join(tokenizer.tokenize(txt)) + ' '
    txt = txt.replace(" won't ", " will n't ")
    txt = txt.replace(" can't ", " can n't ")
    for a in add_space:
        txt = txt.replace(a+' ', ' '+a+' ')

    txt = re.sub(r'^\s+', '', txt)
    txt = re.sub(r'\s+$', '', txt)
    txt = re.sub(r'\s+', ' ', txt)  # remove extra spaces

    return txt
