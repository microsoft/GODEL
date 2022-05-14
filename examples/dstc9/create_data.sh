#!/bin/bash
# ------------------------------------------------------------------
# [Author] Title
#          Description
# ------------------------------------------------------------------

VERSION=0.1.0
SUBJECT=DSTC9
USAGE="Usage: "

# Please clone https://github.com/alexa/alexa-with-dstc9-track1-dataset to download the data.
git clone https://github.com/alexa/alexa-with-dstc9-track1-dataset  
DSTC9_PATH=alexa-with-dstc9-track1-dataset/data
python converter.py ${DSTC9_PATH}