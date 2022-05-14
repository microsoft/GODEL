#!/usr/bin/env python
#  coding=utf-8
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT license.

import json
import random
import copy
import fire
import jsonlines


def process(filepath):
    kbs = json.load(open(f'{filepath}/knowledge.json'))
    import pdb
    examples = []

    random.seed(2022)
    for folder in ['train', 'val']:
        logs = json.load(open(f'{filepath}/{folder}/logs.json'))
        labels = json.load(open(f'{filepath}/{folder}/labels.json'))
        for log, label in zip(logs, labels):

            if label['target']:
                history = [i['text'] for i in log]
                response = label['response']
                kb_str = []
                for kb in label['knowledge']:
                    domain, entity, doc = kb['domain'], kb['entity_id'], kb['doc_id']
                    kb = kbs[domain][str(entity)]['docs'][str(doc)]
                    title, body = kb['title'], kb['body']
                    kb_str.append(f'Q: {title} A: {body}')
                kb_str = ' '.join(kb_str)
                history = ' EOS '.join(history)
                example = {}
                example['Context'] = history
                example['Knowledge'] = kb_str
                example['Response'] = response
                examples.append(copy.deepcopy(example))

        if folder == 'train':
            with jsonlines.open(f'dstc9_{folder}.jsonl', mode='w') as writer:
                for i in examples:
                    if random.random() < 0.025:
                        writer.write(i)
        else:
            with jsonlines.open(f'dstc9_{folder}.jsonl', mode='w') as writer:
                for i in examples:
                    writer.write(i)


def main():
    fire.Fire(process)


if __name__ == '__main__':
    main()
