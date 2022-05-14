#!/bin/bash
# ------------------------------------------------------------------
# [Author] Title
#          Description
# ------------------------------------------------------------------

VERSION=0.1.0
SUBJECT=DialoGLMRedditDataset
USAGE="Usage: "


# Please follow https://microsoft.github.io/msmarco/ to download msmarco dataset
REDDIT_PATH=../data/dummy_data/reddit/dialogpt.t1000.txt


python create_reddit.py ${REDDIT_PATH}