.SECONDARY:

all: train dev valid test refs ../data/grounded-test.refs
data: train dev valid test

refs: ../data/grounded-test.refs.txt
test: ../data/grounded-test.convos.txt ../data/grounded-test.facts.txt
valid: ../data/grounded-valid.convos.txt ../data/grounded-valid.facts.txt
dev: ../data/grounded-dev.convos.txt ../data/grounded-dev.facts.txt
train: ../data/grounded-train.convos.txt ../data/grounded-train.facts.txt

WARGS=--tries=0 --retry-connrefused --waitretry=30

include src/Makefile.official.targets

../data/grounded-test.refs.txt: $(OFFICIAL_TEST_REFS)
	cat $+ | sort | uniq > $@

../data/grounded-test.convos.txt: $(OFFICIAL_TEST_CONVOS)
	cat $+ | sort | uniq > $@

../data/grounded-test.facts.txt: $(OFFICIAL_TEST_FACTS)
	cat $+ > $@

../data/grounded-valid.convos.txt: $(OFFICIAL_VALID_CONVOS)
	cat $+ | sort | uniq > $@

../data/grounded-valid.facts.txt: $(OFFICIAL_VALID_FACTS)
	cat $+ > $@

../data/grounded-dev.convos.txt: $(OFFICIAL_DEV_CONVOS)
	cat $+ > $@

../data/grounded-dev.facts.txt: $(OFFICIAL_DEV_FACTS)
	cat $+ > $@

../data/grounded-train.convos.txt: $(OFFICIAL_TRAIN_CONVOS)
	cat $+ > $@

../data/grounded-train.facts.txt: $(OFFICIAL_TRAIN_FACTS)
	cat $+ > $@

../data/grounded-test.refs: data-official-test/test.refs.txt lists/test-multiref.sets
	cat $< | python src/ids2refs.py lists/test-multiref.sets >  $@

data-official-test/%.refs.txt: data-official-test/%.pkl lists/test-multiref.hashes
	time python src/create_official_data.py --rsinput=reddit/RS_$(*F).zst --rcinput=reddit/RC_$(*F).zst --subreddit_filter=lists/subreddits-official.txt --domain_filter=lists/domains-official.txt --pickle=data-official-test/$(*F).pkl --facts=- --convos=data-official-test/$(*F).refs.txt --anchoronly=True --use_cc=True --test=lists/test-multiref.hashes > logs/$(*F)-refs.log 2> logs/$(*F)-refs.err

## Note: there is no point in removing the '--blind' flag in order to peek at the reference responses (gold), as the organizers will rely on different responses to compute BLEU, etc.
data-official-test/%.facts.txt data-official-test/%.convos.txt data-official-test/%.pkl: reddit/RC_%.zst reddit/RS_%.zst data-official-test/.create lists/test.hashes
	time python src/create_official_data.py --rsinput=reddit/RS_$(*F).zst --rcinput=reddit/RC_$(*F).zst --subreddit_filter=lists/subreddits-official.txt --domain_filter=lists/domains-official.txt --pickle=data-official-test/$(*F).pkl --facts=data-official-test/$(*F).facts.txt --convos=data-official-test/$(*F).convos.txt --anchoronly=True --use_cc=True --test=lists/test.hashes --blind=True > logs/$(*F).log 2> logs/$(*F).err

data-official-valid/%.facts.txt data-official-valid/%.convos.txt: reddit/RC_%.zst reddit/RS_%.zst data-official-valid/.create lists/valid.hashes
	time python src/create_official_data.py --rsinput=reddit/RS_$(*F).zst --rcinput=reddit/RC_$(*F).zst --subreddit_filter=lists/subreddits-official.txt --domain_filter=lists/domains-official.txt --pickle=data-official-valid/$(*F).pkl --facts=data-official-valid/$(*F).facts.txt --convos=data-official-valid/$(*F).convos.txt --anchoronly=True --use_cc=True --test=lists/valid.hashes > logs/$(*F).log 2> logs/$(*F).err

data-official/%.facts.txt data-official/%.convos.txt: reddit/RC_%.zst reddit/RS_%.zst data-official/.create
	time python src/create_official_data.py --rsinput=reddit/RS_$(*F).zst --rcinput=reddit/RC_$(*F).zst --subreddit_filter=lists/subreddits-official.txt --domain_filter=lists/domains-official.txt --pickle=data-official/$(*F).pkl --facts=data-official/$(*F).facts.txt --convos=data-official/$(*F).convos.txt --anchoronly=True --use_cc=True > logs/$(*F).log 2> logs/$(*F).err

data-official-test/.create:
	mkdir -p logs
	mkdir -p data-official-test
	touch $@

data-official-valid/.create:
	mkdir -p logs
	mkdir -p data-official-valid
	touch $@

data-official/.create:
	mkdir -p logs
	mkdir -p data-official
	touch $@

reddit/RS_%.zst:
	mkdir -p logs
	mkdir -p reddit
	wget $(WARGS) https://files.pushshift.io/reddit/submissions/RS_$(*F).zst -O reddit/RS_$(*F).zst -o logs/RS_$(*F).zst.log -c

reddit/RC_%.zst:
	mkdir -p logs
	mkdir -p reddit
	wget $(WARGS) https://files.pushshift.io/reddit/comments/RC_$(*F).zst -O reddit/RC_$(*F).zst -o logs/RC_$(*F).zst.log -c
