---
Title: Tools for thought - Ship's Log 4
Category: Building
Tags: Research, Practices, Discovery
Date: 2026-02-03
Updated: 2026-02-03
Summary: ABC
---

Building on what I learned 
[last time]({filename}/tools-for-thought-ships-log-03.md), I've started in a
new direction but keeping some of the same tooling.

First, I've built out a layout scheme that will replicate (approximately) a vim
file layout of the same size, so that I can run the script in a window next to
vim each time the file changes and then see the nearest neighbors as ideas for
each paragraph in the editor. The end conclusion of this work will be to make a
vim plugin so that I could actually run it in a side-by-side buffer, but for
now I'm happy with what I've got.

Second, I'm working on a new SQLite-based local-first embedding setup. My goal
is that I can download an archive of mixed abstracts, full text PDFs and other
content, then quickly search the database for related documents. This builds on
the previous work for a
["kind downloader"]({filename}/tools-for-thought-ships-log-03.md)

# Embeddings

My target for the embeddings is to have a sentence embedding model that's open
source and runs locally so that I can use it offline to embed new works (new
paragraphs I've written) as I'm going. Most models don't make it over the first
hurdle (open source) or the second (sentence embedding, I'm sure a fixed size
input is easier to deal with).

I thought I'd figured this out with the HuggingFace SentenceTransformers model
`sentence-transformers/all-MiniLM-L6-v2` but I learned this morning when trying
to use it off WiFi that it phones home to HuggingFace and won't initialize
without a connection, it stays stuck in a retry doom loop. I'm working to find
an option where it will cache weights locally so it can start up, otherwise I
will have to find another way.`

# Future Work

Make the live-use tool incremental. I think I can achieve this by caching based
on the paragraph string. Ideally, I can do some steps like normalizing
white space, lowering and something else so that small changes (e.g. fixing a
typo, fixing capitalization) will reuse a cached embedding for fast lookup

Faster Kind Downloads. Store the last download-finished time in a Python shelf
(dict, but backed by a local-on-disk file). If there isn't a value to load from
the shelf, assume three seconds. Otherwise, sleep until 3 seconds have past (or
immediately download if 3 seconds have already passed). As a further
improvement, store this per download URL so that I can manage multiple sources
quickly.

Queue-able downloader. Make a download tool where I can queue up downloading
many different types of content and it will take care of downloading it for me.
My goal is that I can queue things online or offline, then run it again and
download next time I'm online. I'd like to be able to handle things like:
- Take a generic search and download all new results since the last time the script ran
- Take a specific search and download the 1000 newest results
- Eventually, given a URL to a HTML page, download the page locally, get the key content and decimate it to markdown, then ingest the markdown content (with a pointer to the local file)

PDF Support. Given a PDF file locally, extract content, convert to a markdown
document and then ingest. As part of this feature, I'd like it to make a
parallel folder structure with the extracted content in Markdown so I can
review it and make sure that it's sensible. The extracted Markdown can also
serve as a local-available search. After that, the downloader should support,
given a URL to a PDF page, download the PDF so it can do the ingest process.
