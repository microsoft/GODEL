#!/bin/bash
# ------------------------------------------------------------------
# [Author] Title
#          Description
# ------------------------------------------------------------------

VERSION=0.1.0
SUBJECT=DialoGLMRedditDataset
USAGE="Usage: "


# Please follow parlai to download WoW and WoI dataset
# WOW_PATH=/home/bapeng/anaconda3/envs/parlai/lib/python3.8/site-packages/data/wizard_of_wikipedia
# python downstream_tasks_converter.py WoWConverter ${WOW_PATH}

# WOI_PATH=/home/bapeng/anaconda3/envs/parlai/lib/python3.8/site-packages/data/wizard_of_interent
# python downstream_tasks_converter.py WoIConverter ${WOI_PATH}

# # Please follow https://github.com/stanfordnlp/coqa-baselines to prepare seq2seq-train-h2 and seq2seq-dev-h2
# COQA_PATH=/home/bapeng/experiment/cqa/coqa-baselines/data
# python downstream_tasks_converter.py CoQAConverter ${COQA_PATH}

# Please clone https://github.com/wenhuchen/HDSA-Dialog to download the data.
MULTIWOZ_PATH=/home/bapeng/experiment/HDSA-Dialog/data
python downstream_tasks_converter.py MultiWOZConverter ${MULTIWOZ_PATH}