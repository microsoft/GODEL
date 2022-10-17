#!/bin/bash

# Creates trial data for DSTC7 Task 2

mkdir reddit
mkdir data
mkdir logs

TRIAL=`cat lists/data-trial.txt`

for id in $TRIAL; do
	echo Downloading $id
	wget https://files.pushshift.io/reddit/submissions/RS_$id.bz2 -O ../reddit/RS_$id.bz2 -o logs/RS_$id.bz2.log -c
	wget https://files.pushshift.io/reddit/comments/RC_$id.bz2 -O ../reddit/RC_$id.bz2 -o logs/RC_$id.bz2.log -c
	python src/create_trial_data.py --rsinput=../reddit/RS_$id.bz2 --rcinput=../reddit/RC_$id.bz2 --subreddit_filter=lists/subreddits.txt --domain_filter=lists/domains.txt --pickle=data/$id.pkl --facts=data/$id.facts.txt --convos=data/$id.convos.txt > logs/$id.log 2> logs/$id.err
done

eval "cat data/{`echo $TRIAL | sed 's/ /,/g'`}.convos.txt" > data/trial.convos.txt
eval "cat data/{`echo $TRIAL | sed 's/ /,/g'`}.facts.txt" > data/trial.facts.txt
