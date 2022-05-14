#!/usr/bin/env python
#  coding=utf-8
#  Copyright (c) Microsoft Corporation.
#  Licensed under the MIT license.

from abc import ABC, abstractmethod

import jsonlines
import json
import copy
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


class WoWConverter(Converter):

    def process(self):

        train_data = json.load(open(f'{self.filepath}/train.json'))
        topic_data = {}
        for i in train_data:
            chosen_topic = i['chosen_topic']
            if not chosen_topic in topic_data.keys():
                topic_data[chosen_topic] = []
            else:
                topic_data[chosen_topic].append((i['persona'], i['dialog']))

        topic_data_sorted = sorted(
            topic_data.items(), key=lambda k: -len(k[1]))

        examples = []
        for topic, dialogs in topic_data_sorted[1:100:2]:
            for persona, dialog in dialogs[:1]:
                history = [persona]
                history = []
                example = {}
                checked_sentence = ''
                for i in dialog:
                    speaker = i['speaker']
                    text = i['text']
                    if 'Wizard' in speaker:

                        try:
                            checked_sentence = next(
                                iter(i['checked_sentence'].values()))
                        except Exception:
                            checked_sentence = ''
                        response = text
                        example['Context'] = ' EOS '.join(history)
                        example['Knowledge'] = checked_sentence
                        example['Response'] = response.strip()
                        examples.append(copy.deepcopy(example))
                        example = {}
                    else:
                        text = text
                    history.append(text.strip())

        with jsonlines.open('../data/wow/wow_train.jsonl', mode='w') as writer:
            for i in examples:
                writer.write(i)

        for split in ['valid', 'test']:
            data = json.load(
                open(f'{self.filepath}/{split}_random_split.json'))
            examples = []
            for dialog in data:
                history = []
                example = {}
                checked_sentence = ''
                persona = dialog['persona']
                history = [persona]
                for i in dialog['dialog']:
                    speaker = i['speaker']
                    text = i['text']
                    if 'Wizard' in speaker:
                        try:
                            checked_sentence = next(
                                iter(i['checked_sentence'].values()))
                        except Exception:
                            checked_sentence = ''

                        text = text
                        response = text
                        example['Context'] = ' EOS '.join(history)
                        example['Knowledge'] = checked_sentence
                        example['Response'] = response.strip()
                        examples.append(copy.deepcopy(example))
                        example = {}
                    else:
                        text = text
                    history.append(text)

            with jsonlines.open(f'../data/wow/wow_{split}.jsonl', mode='w') as writer:
                for i in examples:
                    writer.write(i)

        return super().process()


class WoIConverter(Converter):

    def process(self):
        for split in ['train', 'valid', 'test']:
            reader = jsonlines.open(f'{self.filepath}/{split}.jsonl')
            examples = []
            num_of_dialogs = 0
            for dialog in reader:
                num_of_dialogs += 1
                example = {}
                history = []
                turn = ''
                data = list(dialog.values())[0]
                persona = data['apprentice_persona']
                history = [persona.replace('\n', ' ')]

                for i in data['dialog_history']:
                    if 'SearchAgent' in i['action']:
                        continue

                    else:
                        if i['action'] == 'Wizard => Apprentice':

                            contents = []
                            selected = []

                            for content_ in i['context']['contents']:
                                contents.extend(content_['content'])

                            for selected_ in i['context']['selected_contents']:
                                selected.extend(selected_)

                            knowledge = []
                            for c, s in zip(contents, selected[1:]):
                                if s:
                                    knowledge.append(c)

                            turn = i['text'].strip()
                            example['Context'] = ' EOS '.join(history)
                            example['Knowledge'] = ' '.join(knowledge)
                            example['Response'] = turn.strip()
                            examples.append(copy.deepcopy(example))
                        else:
                            turn = i['text'].strip()
                        history.append(turn)

            with jsonlines.open(f'../data/woi/woi_{split}.jsonl', mode='w') as writer:
                for i in examples:
                    if split == 'train':
                        if random.random() < 0.006:
                            writer.write(i)
                    else:
                        writer.write(i)

        return super().process()


class CoQAConverter(Converter):

    def process(self):

        for split in ['train', 'dev']:
            source = open(f'{self.filepath}/seq2seq-{split}-h2-src.txt')
            target = open(f'{self.filepath}/seq2seq-{split}-h2-tgt.txt')

            source_ = []
            for line in source:
                if line.strip() != '':
                    sotry, question = line.strip().split('||')
                    source_.append((sotry, question))

            target_ = []
            for line in target:
                if line.strip() != '':
                    target_.append(line.strip())
            examples = []
            for context, response in zip(source_, target_):
                story, question = context
                examples.append(
                    {'Context': question, 'Response': response, 'Knowledge': story})

            if split == 'dev':
                split = 'valid'
            with jsonlines.open(f'../data/coqa/coqa_{split}.jsonl', mode='w') as writer:
                for i in examples:
                    if split == 'train':
                        if random.random() < 0.006:
                            writer.write(i)
                    else:
                        writer.write(i)

        return super().process()


class MultiWOZConverter(Converter):

    def process(self):

        for split in ['train', 'val', 'test']:
            data = json.load(open(f'{self.filepath}/{split}.json'))
            examples = []
            for i in data:
                name = i['file'].lower()
                history = []
                for turn in i['info']:
                    history.append(turn['user_orig'])
                    bs = turn['BS']
                    bs_str = []
                    for domain, states in bs.items():
                        domain_str = []
                        for state in states:
                            domain_str.append(state[0] + ' = ' + state[1])
                        domain_str = ' ; '.join(domain_str)
                        bs_str.append(domain + ' ' + domain_str)
                    bs_str = ' | '.join(bs_str)

                    db_str = 'kb '
                    db = turn['KB']
                    if db == 0:
                        db_str += 'zero'
                    elif db_str == 1:
                        db_str += 'one'
                    elif db_str == 2:
                        db_str += 'two'
                    else:
                        db_str += 'more than two'

                    act_seq = ' '.join(turn['act'].keys())
                    example = {}
                    example['Context'] = ' EOS '.join(history[:])
                    example['Knowledge'] = bs_str + ' | ' + db_str
                    example['Response'] = act_seq + ' | ' + turn['sys'].strip()

                    history.append(turn['sys'].strip())
                    examples.append(copy.copy(example))

            if split == 'val':
                split = 'valid'
            with jsonlines.open(f'../data/multiwoz/multiwoz_{split}.jsonl', mode='w') as writer:
                for i in examples:
                    if split == 'train':
                        if random.random() < 0.006:
                            writer.write(i)
                    else:
                        writer.write(i)

        return super().process()


def convert(class_name, file_path):
    eval(class_name)(file_path).convert()


def main():
    fire.Fire(convert)


if __name__ == '__main__':
    main()
