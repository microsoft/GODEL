#!/usr/bin/env python
#  coding=utf-8
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT license.

from abc import ABC, abstractmethod

import jsonlines
import json
import copy
import glob
import random
import fire


class Converter(ABC):

    def __init__(self, filepath) -> None:
        super().__init__()

        self.filepath = filepath

    def convert(self):
        """
        Implement your convert logics in this function
        """
        self.start()
        self.process()
        self.end()
        pass

    def start(self):
        print(f'Start processing {self.__class__.__name__} at {self.filepath}')

    def end(self):
        print(
            f'Finish processing {self.__class__.__name__} at {self.filepath}')

    @abstractmethod
    def process(self):
        """
        Implement your convert logics in this function
        """


class DSTC7Converter(Converter):

    '''
    Converter class for DSTC7 Grounded response generation
    '''

    def process(self):

        convs = open(self.filepath)
        examples = []
        for conv in convs:
            _, c_id, score, facts, context, response = conv.split('\t')
            example = {}
            if context.strip() == 'START':
                continue
            context = context.replace('START EOS TIL ', '')
            example['Context'] = context.strip()
            example['Knowledge'] = facts.replace(
                ' < p > ', '').replace(' < /p > ', '').strip()
            example['Response'] = response.strip()
            examples.append(copy.deepcopy(example))

        with jsonlines.open('../data/dstc7.jsonl', mode='w') as writer:
            for i in examples:
                writer.write(i)

        return


class MSMARCOConverter(Converter):

    '''
    Converter class for MS MARCO 
    '''

    def process(self):

        train_data = json.load(open(self.filepath))
        examples = []
        for ids in train_data['query'].keys():
            query, answer, passage = train_data['query'][ids], train_data['answers'][ids], train_data['passages'][ids]
            knowledge = [i['passage_text']
                         for i in passage if i['is_selected']]
            example = {}
            example['Context'] = query.strip()
            example['Knowledge'] = ' '.join(knowledge)
            example['Response'] = ' '.join(answer).strip()
            examples.append(copy.deepcopy(example))

        with jsonlines.open('../data/msmarco.jsonl', mode='w') as writer:
            for i in examples:
                writer.write(i)

        return


class UnifiedQAConverter(Converter):

    def process(self):

        examples = []
        for fname in glob.glob(f'{self.filepath}/*/*'):
            if 'train.tsv' in fname or 'test.tsv' in fname:
                data = open(fname)
                for line in data:
                    line = line.strip()
                    try:
                        question, answer = line.split('\t')
                        question, story = question.split('\\n')
                        example = {}
                        example['Context'] = question
                        example['Response'] = answer
                        example['Knowledge'] = story
                        examples.append(copy.deepcopy(example))
                        k += 1
                    except:
                        pass

        train_writer = jsonlines.open('../data/unifiedqa.jsonl', mode='w')
        for i in examples:
            train_writer.write(i)

        return


class SGDConverter(Converter):

    '''
    Converter class for SGD dataset
    '''

    def process(self):

        examples = []
        for split in ['train', 'dev', 'test']:
            schema_info = json.load(
                open(f'{self.filepath}/{split}/schema.json'))
            schema_info = dict([(i['service_name'], i) for i in schema_info])
            for file in glob.glob(f'{self.filepath}/{split}/dialogues_*.json'):
                data = json.load(open(file))
                for dialogue in data:
                    dialogue_id = dialogue['dialogue_id']
                    services = dialogue['services'][0]
                    schema = schema_info[services]
                    description = schema['description']
                    task_slots = [s['name'] for s in schema['slots']]
                    task_intents = [s['name'] for s in schema['intents']]
                    task_intents_description = [
                        s['description'] for s in schema['intents']]
                    turns = dialogue['turns']
                    history = []
                    example = {}
                    for idx, turn in enumerate(turns):
                        if idx == 0:
                            assert turn['speaker'] == 'USER'
                        frame = turn['frames'][0]
                        service = turn['frames'][0]['service'].split('_')[
                            0].lower()
                        if turn['speaker'] == 'USER':
                            user_utter = turn['utterance']
                            history.append(f'{user_utter}')
                            belief_slot_values = frame['state']['slot_values']
                            slot_values_list = []
                            for slot_value in belief_slot_values.items():
                                slot, values = slot_value
                                value = values[0]
                                slot_values_list.append(f'{slot} = {value}')
                            slot_values_str = ' ; '.join(slot_values_list)

                        else:
                            sys_utter = copy.copy(turn['utterance'])
                            slot_values_str = f'belief : {service} {slot_values_str}'

                            slots = frame['slots']
                            offset = 0
                            len_ = len(sys_utter)
                            candidates = []
                            for idx, slot_info in enumerate(slots):
                                start, end, slot_name = slot_info['start'], slot_info['exclusive_end'], slot_info['slot']
                                sys_utter = sys_utter[:start+offset] + str(
                                    idx) * (end - start) + sys_utter[end+offset:]
                                candidates.append(
                                    (slot_name, str(idx) * (end - start)))
                            for idx, info in enumerate(candidates):
                                slotname, target = info
                                sys_utter = sys_utter.replace(
                                    target, f'[{slotname}]')

                            reply = f'{sys_utter}'
                            example['Context'] = ' EOS '.join(history)
                            example['Knowledge'] = slot_values_str
                            example['Response'] = reply
                            examples.append(copy.deepcopy(example))
                            history.append(reply)

        train_writer = jsonlines.open('../data/sgd.jsonl', mode='w')
        for i in examples:
            train_writer.write(i)

        return


def merge_and_split():

    examples = []
    filepath = '../data/dstc7.jsonl'
    with open(filepath, "r", encoding="utf-8") as reader:
        for item in jsonlines.Reader(reader):
            examples.append(item)

    filepath = '../data/msmarco.jsonl'
    with open(filepath, "r", encoding="utf-8") as reader:
        for item in jsonlines.Reader(reader):
            examples.append(item)

    filepath = '../data/sgd.jsonl'
    with open(filepath, "r", encoding="utf-8") as reader:
        for item in jsonlines.Reader(reader):
            examples.append(item)

    filepath = '../data/unifiedqa.jsonl'
    with open(filepath, "r", encoding="utf-8") as reader:
        for item in jsonlines.Reader(reader):
            examples.append(item)

    random.seed(2021)
    train_writer = jsonlines.open(
        '../data/grounded_data_train.jsonl', mode='w')
    valid_writer = jsonlines.open(
        '../data/grounded_data_valid.jsonl', mode='w')
    for i in examples:
        if random.random() < 0.01:
            valid_writer.write(i)
        else:
            train_writer.write(i)

    print('Done!')


def process(
    msmarco_path,
    sgd_path,
    dstc7_path,
    unified_qa_path
):
    MSMARCOConverter(f'{msmarco_path}/train_v2.1.json').convert()
    SGDConverter(f'{sgd_path}').convert()
    DSTC7Converter(f'{dstc7_path}').convert()
    UnifiedQAConverter(unified_qa_path).convert()


def main():
    fire.Fire(process)
    # merge generated data and split it into train and valid
    merge_and_split()


if __name__ == '__main__':
    main()
