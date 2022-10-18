# Data Extraction for DSTC7: End-to-End Conversation Modeling 

Task 2 uses conversational data extracted from Reddit. Each conversation in this setup is _grounded_, as each conversation in this data is about a specific web page that was linked at the start of the conversation. This page provides code to extract the data from a Reddit [dump](http://files.pushshift.io/reddit/comments/) and from [Common Crawl](http://commoncrawl.org/). The former data provides the conversation, while the latter offers the grounding. We provide code instead of actual data, as we are unable to directly release this data.

(Note: the older and now obsolete setup to create the "trial" data can be found [here](https://github.com/DSTC-MSR/DSTC7-End-to-End-Conversation-Modeling/tree/master/data_extraction/trial).)

If you run into any problem creating the data, please check the [FAQ](https://github.com/mgalley/DSTC7-End-to-End-Conversation-Modeling/tree/master/data_extraction#FAQ) section below.

## Requirements

This page assumes you are running a UNIX environment (Linux, macOS, etc.) If you are on Windows, please either use its Ubuntu subsystem (instructions [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10)) or any third-party UNIX-like environment such as [Cygwin](https://www.cygwin.com/). Creating the data requires a fair amount of disk space to store Reddit dump files locally, i.e., 500 GB total. You will also need the following programs:

* `Python 3.x`, with modules:
   * `nltk`
   * `beautifulsoup4`
   * `chardet`
   * `zstandard`
* `make`

To install the above Python modules, you can run:

```pip install -r requirements.txt```

Please also run set `PYTHONIOENCODING=UTF-8` in your environment, e.g., by running this in bash:
```export PYTHONIOENCODING=UTF-8``

## Create official data (train and dev):

First, make sure that Python and all required modules are installed, for example by generating a subset of the data (January 2011):

```make data-official/2011-01.convos.txt```

If the target file is missing after running that command, that probably means Python or one of its modules is missing, is the wrong version, or is misconfigured. Please inspect logs files in `logs/*.log` or `logs/*.err` to find the cause of the problem (please refer to the "Requirements" section above). 

If everything is setup properly, please run the following command to create the official training data:

```make -j4```

This will run the extraction pipeline with 4 processes. Depending on your number of cores on your machine, you might want to increase or descrease that number. This will take 2-5 days to run, depending on the number of processes selected. This will create two tab-separated (tsv) files `data/train.convos.txt` and `data/train.facts.txt`, which respectively contain the conversational data and grounded text ("facts"). This will also create two files for the dev set.

The data is generated from Reddit and the web, so some of it is noisy and occasionally contains offensive language. While we mostly selected Reddit boards (i.e., "subreddits") and web domains that are mostly "safe for work", explicit and offensive language sometimes appears in the data and we did not attempt to eliminate it further (for the sake of simplicity and reproducibility of our pipeline).

Note: if you set a large number of processes, the server hosting the Reddit data (`files.pushshift.io`) might complain about "too many open connections". If so, you might want to use the makefile to first create all `reddit/*.zst` files and only then run e.g. `make -j7`.

Generated data files (see data description below):
1. `train.convos.txt`: Conversations of the training set
2. `train.facts.txt`: Facts of the training set
3. `dev.convos.txt`: Conversations of the dev set
4. `dev.facts.txt`: Facts of the dev set

Role of each dataset:
1. TRAIN: do anything you want with this data (train, analyze, etc.);
2. DEV: you may tune model hyperparameters on this data, but you may NOT train any model directly on that;
3. TEST (official release Sept 10): The blind test set will provide facts and conversational contexts, but the gold responses will be hidden (replaced with `__UNDISCLOSED__`). 

If you participate in the challenge and plan to send us system outputs, **please do NOT use any other training data**, other than the data provided on this page.

## Data description:

Each conversation in this dataset consist of Reddit `submission` and its following discussion-like `comments`. In this data, we restrict ourselves to submissions that provide a `URL` along with a `title` (see [example Reddit submission](https://www.reddit.com/r/todayilearned/comments/f2ruz/til_a_woman_fell_30000_feet_from_an_airplane_and/), which refers to [this web page](https://en.wikipedia.org/wiki/Vesna_Vulovi%C4%87)). The web page scraped from the URL provides grounding or context to the conversation, and is additional (non-conversational) input that models can condition on to produce responses that are more informative and contentful. 

### Conversation file:

Each line of `train.convos.txt` and `dev.convos.txt` contains a Reddit response and its preceding conversational context. Long conversational contexts are truncated by keeping the last 100 words. The file contains 5 columns:

1. hash value (only for sanity check)
2. subreddit name
3. conversation ID
4. response score
5. dialogue turn number (e.g., "1" = start of the conversation, "2" = 2nd turn of a conversation)
6. conversational context, usually multiple turns (input of the model)
7. response (output of the model)

The converational context may contain:
* EOS: special symbol indicating a turn transition
* START: special symbol indicating the start of the conversation

### Facts file:

Each line of `train.facts.txt` and `dev.facts.txt` contains a "fact", either a sentence, paragraph (or other snippet of text) relevant to the current conversation. Use conversation IDs to find the facts relevant to each conversation. Note: facts relevant to a given conversation are ordered as they appear on the original web page. The file contains 3 columns:

1. hash value (only for sanity check)
2. subreddit name
3. conversation ID
4. domain name
5. fact

To produce the facts relevant to each conversation, we extracted the text of the page using an html-to-text converter ([BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)), but kept the most important tags intact (`<title>, <h1-6>, <p>, etc`). As web formatting differs substantially from domain to domain and common tags like `<p>` may not be used in some domains, we decided to keep all the text of the original page (however, we do remove javascript and style code). As some of the fact data tend to be noisy, you may want restrict yourself to facts delimited by these tags.


#### Labeled anchors

A substantial number of URLs contain labeled achors, for example:

```http://en.wikipedia.org/wiki/John_Rhys-Davies#The_Lord_of_the_Rings_trilogy```

which here refers to the label `The_Lord_of_the_Rings_trilogy`. This information is preserved in the facts, and indicated with the tags `<anchor>` and `</anchor>`. As many web pages in this dataset are lengthy, anchors are probably useful information, as they indicate what text the model should likely attend to in order to produce a good response.

### Data statistics:

|                   | Trial data    |   Train set | Dev set |
| ----              | ----          |   ----      | ----    |
|# dialogue turns   |   649,866     |   2,364,228 | -       |
|# facts            | 4,320,438     |  15,180,800 | -       |
|# tagged facts (1) |   998,032     |   2,185,893 | -       |

(1): facts tagged with html markup (e.g., <title>) and therefore potentially important.

### Sample data:

#### Sample conversation turn:

```<hash> \t todayilearned \t f2ruz \t 145 \t 2 \t START EOS til a woman fell 30,000 feet from an airplane and survived . \t the page states that a 2009 report found the plane only fell several hundred meters .```

Maps to:

1. hash value: ...
2. subreddit name: `TodayILearned`
3. conversation ID: `f2ruz`
4. response score: `145`
5. dialogue turn number: `2`
6. conversational context: `START EOS til a woman fell 30,000 feet from an airplane and survived .`
7. response: `the page states that a 2009 report found the plane only fell several hundred meters .`

#### Sample fact:

```<hash> \t todayilearned \t f2ruz \t en.wikipedia.org \t <p> four years later , peter hornung-andersen and pavel theiner , two prague-based journalists , claimed that flight 367 had been mistaken for an enemy aircraft and shot down by the czechoslovak air force at an altitude of 800 metres ( 2,600 ft ) . </p>```

Maps to:
1. hash value: ...
2. subreddit name: `TodayILearned`
3. conversation ID: `f2ruz`
4. domain name: `en.wikipedia.org`
5. fact: `<p> four years later , peter hornung-andersen and pavel theiner , two prague-based journalists , claimed that flight 367 had been mistaken for an enemy aircraft and shot down by the czechoslovak air force at an altitude of 800 metres ( 2,600 ft ) . </p>`

<a name="FAQ"></a>
## FAQ

**Q:** `make` crashed and returned some non-zero code(s), e.g.: `make: *** [reddit/RC_2013-05.zst] Error 8`
<br>
**A:** It might be a temporary network connection problem. If you rerun the same `make` command, the scripts will resume data download and creation from where it left off. 
<br>
**A:** Alternatively, it might be because you ran `make` with a large number of processes (> 4). The server hosting the Reddit data doesn't allow more than 4 simultaneous connections from the same IP address.

**Q:** Creating the data with these scripts is inconvenient. Instead, could you please send us the data directly?
<br>
**A:** The data (either Reddit or web) is not our own, so we are unable to redistribute it. The same situtation happended last year for [DSTC6 Task 2](https://github.com/dialogtekgeek/DSTC6-End-to-End-Conversation-Modeling), and the organizers then also provided scraping code that let participants construct the data themselves.

**Q:** I have trouble running the download script because of Internet control in my country. 
<br>
**A:** You might want to consider VPN solutions. Alternatively, you could try to team up with other people or team who live in a different country. Participants from different institutions can collaborate and submit system outputs together. 

