#!/bin/bash
# ------------------------------------------------------------------
# [Author] Title
#          Description
# ------------------------------------------------------------------

VERSION=0.1.0
SUBJECT=DialoGLMGroundedDataset
USAGE="Usage: "


# Please follow https://microsoft.github.io/msmarco/ to download msmarco dataset
MSMARCO_PATH=/home/bapeng/experiment/DialoGLM/data/dummy_data/msmarco 

# Please follow https://github.com/google-research-datasets/dstc8-schema-guided-dialogue
SGD_PATH=/home/bapeng/experiment/dstc8-schema-guided-dialogue 

# Please follow https://github.com/mgalley/DSTC7-End-to-End-Conversation-Modeling
DSTC7_PATH=/home/bapeng/experiment/DialoGLM/data/dummy_data/dstc7/dstc7_h100.tsv 

#Please follow instructions on https://github.com/allenai/unifiedqa to download the dataset
UNIFIED_QA_PATH=/home/bapeng/experiment/DialoGLM/data/dummy_data/unifedqa

python grounded_converter.py ${MSMARCO_PATH} ${SGD_PATH} ${DSTC7_PATH} ${UNIFIED_QA_PATH}