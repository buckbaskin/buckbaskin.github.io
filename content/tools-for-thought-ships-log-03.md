---
Title: Tools for thought - Ship's Log 3
Category: Building
Tags: Research, Practices, Discovery
Date: 2025-02-21
Updated: 2025-02-25
Summary: Building on the learnings from last time, I'm working on improving the download experience. The previous experience was somewhat limited when trying to incorporate new sources.
---

Building on the learnings from 
[last time]({filename}/tools-for-thought-ships-log-02.md), I'm working on
improving the download experience. The previous experience was somewhat limited
when trying to incorporate new sources.

# Nicer Downloading

The primary focus was adding bulk downloads for existing topics. Now I can use
one script, point it at an arXiv category like robotics ("cs.RO") and get 100s
or 1000s of recent results.

Following from that, it was pretty easy to extend this to a one-stop
configuration-based script where I can easily run a single daily command to
pick up papers on a range of interesting topics.

# Markdown parsing - Part 2
[Part 1]({filename}/tools-for-thought-ships-log-01.md#markdown-parsing)

I've partially implemented the vision for Markdown parsing as part of loading
documents. The current simplified version just reduces the content down to
plain text to remove some of the extraneous content. In the future, it'll
require a little more reworking to parse out the document into a structured
tree of texts to allow stacking context for each paragraph instead of treating
each as an independent document.

The simplified version of this tree of topics would be to start with using the
"topic" provided to the interactive.py script as a context for each document
(which is itself not clear how I'd achieve that but seems like an interesting
project)

# Other Improvements I'm Considering

## Manual Entry

I'd like to make a nice way to manually add in papers that I've read that
predate the existing tooling so I can incorporate them into search as well

## Semantic Search

I'd like to be able to search by topic (or topics) in the database using the
embeddings

## Baseline Search

I'd also like to spin up a
[TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) search tool so I can
have a consistent baseline for comparing if the embedding-based search is
finding the documents that I'd like to find. I'll stick with embedding search
if the documents it surfaces consistently are more "interesting" than the
baseline; otherwise, it may make sense pursuing alternate embeddings to improve
search quality.

## Other Sources

This approach has a fairly generic interface (anything that can be chunked as
one or more paragraphs of text can be used), so I'd like to consider expanding
to other sources. For example, discussions on Mastodon could be a good way to
explore new topics

## User Labelling

I'd like to be able to (easily) add labels to documents such as "downloaded",
"read", "liked" and then use that to drive recommendations (e.g. for each
document predict the likelihood that I'd download, read and/or like the paper).
This would allow me to use nearest neighbors voting to estimate the value I'd
get from new papers when exploring existing topics.

## Performance Improvements

One of the startup costs I haven't found a good way to reduce is the initial
save cost. The embeddings are roughly going to be what they are, but I'm
wondering if I could get better performance by inserting scikit-learn's
[K-nearest neighbors regression](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html)
tooling into the database for faster lookup (and maybe faster insert too?).
