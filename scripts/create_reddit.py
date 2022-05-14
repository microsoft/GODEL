#!/usr/bin/env python
#  coding=utf-8
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT license.

import jsonlines
import fire


def _norm_text(text):
    w, *toks = text.strip().split()
    try:
        w = float(w)
    except Exception:
        toks = [w] + toks
        w = 1.0
    return w, ' '.join(toks)


def _get_inputs_from_text(text):
    srcs, tgt = text.strip().split('\t')
    weights = []
    inputs = []
    for src in srcs.split(' EOS '):
        src_weight, src = _norm_text(src)
        weights.append(src_weight)
        inputs.append(src)
    tgt_weight, tgt = _norm_text(tgt)
    if tgt_weight != 0:
        weights.append(tgt_weight)
        inputs.append(tgt)
    return weights, inputs


def process(reddit_path):

    idx = 0
    writer = jsonlines.open('../data/reddit_session_level.jsonl', 'w')
    with open(reddit_path, "r", encoding="utf-8") as reader:
        for line in reader:
            idx += 1
            if idx % 10000 == 0:
                print(idx)
            weights, inputs = _get_inputs_from_text(line)
            if 0.0 in weights:
                continue
            else:
                writer.write({'text': ' EOS '.join(inputs)})

    idx = 0
    with open('../data/reddit_session_level.jsonl', "r", encoding="utf-8") as reader:
        writer = jsonlines.open('../data/reddit.jsonl', mode='w')
        for item in jsonlines.Reader(reader):
            idx += 1
            if idx % 10000 == 0:
                print(idx)
            context = item['text'].split('EOS')

            for idx in range(0, len(context)-1):

                history = 'EOS'.join(context[:idx+1])
                response = context[idx+1]

                if len(history) == 0:
                    continue

                example = {}
                example['Context'] = history
                example['Knowledge'] = ''
                example['Response'] = response.strip()

                writer.write(example)


def main():
    fire.Fire(process)


if __name__ == '__main__':
    main()
