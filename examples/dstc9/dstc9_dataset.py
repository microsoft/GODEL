#!/usr/bin/env python
#  coding=utf-8
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT license.

"""Corpus for DSTC9"""

import datasets
import jsonlines


_DESCRIPTION = """\
DSTC9
"""

_CITATION = """\
DSTC9
"""

_WEBPAGE = ""


class DSTC9(datasets.GeneratorBasedBuilder):
    """DSTC9"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "Context": datasets.Value("string"),
                    "Response": datasets.Value("string"),
                    "Knowledge": datasets.Value("string"),
                }
            ),
            homepage=_WEBPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        train_path = '../examples/dstc9/dstc9_train.jsonl'
        validation_path = '../examples/dstc9/dstc9_val.jsonl'
        test_path = '../examples/dstc9/dstc9_val.jsonl'
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={
                                    "filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={
                                    "filepath": validation_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={
                                    "filepath": test_path}),
        ]

    def _generate_examples(self, filepath):

        key = 0
        with open(filepath, "r", encoding="utf-8") as reader:

            for item in jsonlines.Reader(reader):
                yield key, item
                key += 1
