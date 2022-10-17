# Data Extraction for DSTC7: End-to-End Conversation Modeling 

Task 2 uses conversational data extracted from Reddit, along with the text of the link that started these conversations. This page provides scripts to extract the data from a Reddit [dump](http://files.pushshift.io/reddit/comments/), as we are unable to release the data directly ourselves.

*Note: In the original proposal, we planned to use Twitter data (conversational data) and Foursquare (grounded data), but decided to use Reddit, owing to the volatility of Twitter data, as well the technical difficulties of aligning Twitter content with data from other sources. Reddit provides an intuitive direct link to external data in the submissions that can be utilized for this task.*

## Requirements

* `Python 3.x`, with modules:
   * `nltk`
   * `beautifulsoup4`
* `make`
* `wget`


## Create trial data:

To create the trial data, please run:

```src/create_trial_data.sh```

This will create two tab-separated (tsv) files `data/trial.convos.txt` and `data/trial.facts.txt`, which respectively contain the conversational data and grounded text ("facts"). This requires about 20 GB of disk space.

### Notes:

* **Web crawling**: The above script downloads grounding information directly from the web, but does respect the servers' `robots.txt` rules. The official version of the data (forthcoming) will extract that data from [Common Crawl](http://commoncrawl.org/), to ensure that all participants use exactly the same data, and to minimize the number of dead links.
* **Data split**: The official data will be divided into train/dev/test, but the trial data isn't.
* **Offensive language**: We restricted the data to subreddits that are generally inoffensive. However, even the most "well behaved" subreddits occasionally contain offensive and explicit language, and the trial-version of the data does not attempt to remove it.

## Data description:

Each conversation in this dataset consist of Reddit `submission` and its following discussion-like `comments`. In this data, we restrict ourselves to submissions that provide an `URL` along with a `title` (see [example Reddit submission](https://www.reddit.com/r/todayilearned/comments/f2ruz/til_a_woman_fell_30000_feet_from_an_airplane_and/), which refers to [this web page](https://en.wikipedia.org/wiki/Vesna_Vulovi%C4%87)). The web page scraped from the URL provides grounding or context to the conversation, and is additional (non-conversational) input that models can condition on to produce responses that are more informative and contentful. 

### Conversation file:

Each line of `trial.convos.txt` contains a Reddit response and its preceding conversational context. Long conversational contexts are truncated by keeping the last 100 words. The file contains 5 columns:

1. subreddit name
2. conversation ID
3. response score
4. conversational context, usually multiple turns (input of the model)
5. response (output of the model)

The converational context may contain:
* EOS: special symbol indicating a turn transition
* START: special symbol indicating the start of the conversation

### Facts file:

Each line of `trial.facts.txt` contains a "fact", either a sentence, paragraph (or other snippet of text) relevant to the current conversation. Use conversation IDs to find the facts relevant to each conversation. Note: facts relevant to a given conversation are ordered as they appear on the original web page. The file contains 3 columns:

1. subreddit name
2. conversation ID
3. fact

To produce the facts relevant to each conversation, we extracted the text of the page using an html-to-text converter ([BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)), but kept the most important tags intact (`<title>, <h1-6>, <p>, etc`). As web formatting differs substantially from domain to domain and common tags like `<p>` may not be used in some domains, we decided to keep all the text of the original page (however, we do remove javascript and style code). As some of the fact data tend to be noisy, you may want restrict yourself to facts delimited by these tags.


#### Labeled anchors

A substantial number of URLs contain labeled achors, for example:

```http://en.wikipedia.org/wiki/John_Rhys-Davies#The_Lord_of_the_Rings_trilogy```

which here refers to the label `The_Lord_of_the_Rings_trilogy`. This information is preserved in the facts, and indicated with the tags `<anchor>` and `</anchor>`. As many web pages in this dataset are lengthy, anchors are probably useful information, as they indicate what text the model should likely attend to in order to produce a good response.

### Data statistics:

|                   | Trial data    | Train set | Dev set | Test set |
| ----              | ----          | ----      | ----    | ----     |
|# dialogue turns   |   649,866     | -         | -       | -        |
|# facts            | 4,320,438     | -         | -       | -        |
|# tagged facts (1) |   998,032     | -         | -       | -        |

(1): facts tagged with html markup (e.g., <title>) and therefore potentially important.

### Sample data:

#### Sample conversation turn (from trial.convos.txt):

```todayilearned \t f2ruz \t 145 \t START EOS til a woman fell 30,000 feet from an airplane and survived . \t the page states that a 2009 report found the plane only fell several hundred meters .```

Maps to:
1. subreddit name: `TodayILearned`
2. conversation ID: `f2ruz`
3. response score: `145`
4. conversational context: `START EOS til a woman fell 30,000 feet from an airplane and survived .`
5. response: `the page states that a 2009 report found the plane only fell several hundred meters .`

#### Sample fact (from trial.facts.txt):

```todayilearned \t f2ruz \t <p> four years later , peter hornung-andersen and pavel theiner , two prague-based journalists , claimed that flight 367 had been mistaken for an enemy aircraft and shot down by the czechoslovak air force at an altitude of 800 metres ( 2,600 ft ) . </p>```

Maps to:
1. subreddit name: `TodayILearned`
2. conversation ID: `f2ruz`
3. fact: `<p> four years later , peter hornung-andersen and pavel theiner , two prague-based journalists , claimed that flight 367 had been mistaken for an enemy aircraft and shot down by the czechoslovak air force at an altitude of 800 metres ( 2,600 ft ) . </p>`
