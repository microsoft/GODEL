#!/usr/bin/env python
#  coding=utf-8
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT license.

import torch
import numpy as np
import dotmap

from transformers import (
    AutoConfig,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)


def set_seed(args):
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)


model = None
tokenizer = None
args = dotmap.DotMap()
args.model_name_or_path = 't5-base'
args.prompt = ''
args.padding_text = ''
args.length = 128
args.num_samples = 1
args.temperature = 1
args.num_beams = 5
args.repetition_penalty = 1
args.top_k = 0
args.top_p = 0.5
args.no_cuda = False
args.seed = 2022
args.stop_token = '<|endoftext|>'
args.n_gpu = 1
args.device = 'cuda:0'

set_seed(args)


def main():
    global model, tokenizer, args

    config = AutoConfig.from_pretrained(args.model_name_or_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        args.model_name_or_path,
        from_tf=bool(".ckpt" in args.model_name_or_path),
        config=config,
    )

    model = model.to(args.device)
    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name_or_path, use_fast=not args.use_slow_tokenizer)


def generate(context, knowledge):
    global model, args, tokenizer

    input_ids = tokenizer(context + ' <|knowledge|> ' + knowledge +
                          ' =>', return_tensors="pt").input_ids.to(args.device)
    gen_kwargs = {
        # 'num_beams': args.num_beams,
        'max_length': args.length,
        'min_length': 32,
        'top_k': 10,
        'no_repeat_ngram_size': 4

    }

    output_sequences = model.generate(input_ids, **gen_kwargs)
    output_sequences = tokenizer.batch_decode(
        output_sequences, skip_special_tokens=True)

    return output_sequences


if __name__ == '__main__':
    main()
