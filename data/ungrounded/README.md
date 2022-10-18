### Data Preparation

The first step to retrain the full models is to generate the DialoGPT 27GB Reddit dataset. This involves downloading full Reddit submission and comments dumps from [https://files.pushshift.io/reddit](https://files.pushshift.io/reddit) and creating intermediate files, which overall require **700GB of local disk space**. Downloading and processing the full data requires about 1-2 days, depending on your (CPU) compute capabilties (e.g., ~24 hours with 8 cores on a recent computer). Assuming you ran the above setup and installation steps (conda activate LSP, etc.), you can create the full dataset by running:

```
SIZE=full make -j 8
```

Note that the downloading phase can be error prone, for example based on your geolocation (firewall, etc.). If the above commands fail to generate `data/train.tsv`, or if that file is not anywhere close to 27GB, it means something went wrong. In that case, you may want to inspect `reddit_extractor/wget-log` and `reddit_extractor/logs/*.log` for any obvious error (e.g., wget unable to download from pushshift.io). If error messages don't make sense to you, feel free to contact us. If so, please be sure to include any error messages gathered from these log files.

Training data statistics: the generated training tsv file should be roughly 26.8 GB uncompressed, with 146.8M training instances, 3.87B source tokens, and 2.14B target tokens (including utterance-level 0/1 weights). The resulting train.tsv file should contain 146,846,215 lines.
