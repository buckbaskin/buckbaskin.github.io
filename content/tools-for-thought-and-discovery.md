---
Title: Tools for thought and discovery
Category: Building
Tags: Research, Practices, Discovery
Date: 2025-02-14
Updated: 2025-02-14
Summary: I've always been interested in increasing the number of research papers that I read and using that to speed up how quickly I can learn different knowledge areas. The problem I have is that I'm aware of large sources of papers (e.g. Mastodon, arXiv.org, and toward my specific interests, the robotics and software engineering topics within arXiv), but don't know what I don't know about content that I'm missing. Where I'd like to end up is that I can be working on writing a topic and in parallel tools can be working to help me surface references that can either be immediately cited or extend my learning on the topic in a tight loop with my writing.
---

I've always been interested in increasing the number of research papers that I
read and using that to speed up how quickly I can learn different knowledge
areas.

This continues the Discovery angle from the post 
[Research Areas for 2025](blog/research-areas-for-2025.html)

The problem I have is that I'm aware of large sources of papers (e.g. Mastodon,
arXiv.org, and toward my specific interests, the robotics and software
engineering topics within arXiv), but don't know what I don't know about
content that I'm missing. Where I'd like to end up is that I can be working on
writing a topic and in parallel tools can be working to help me surface
references that can either be immediately cited or extend my learning on the
topic in a tight loop with my writing.

An example of where I've ended up so far:

# Example

The tool can be run something like this

```
$ echo content/research-areas.md | entr python interactive.py compiler content/research-areas-for-2025.md 
```

A quick aside, `entr` is a tool that runs the given command when the file (or
files) change.  There's an option to include a topic as context, but I haven't
gotten to using it for anything helpful yet

Taking some example content from the post
[Research Areas for 2025](blog/research-areas-for-2025.html)

```
## Drones

- Visual Odometry
- Visual Inertial Odometry
- VI SLAM w/ Factor Graphs
```

The tool outputs a recommendation like the following (currently per-paragraph)

```
=== Content Batch 6 ===
- Visual Odometry - Visual Ine...try - VI SLAM w/ Factor Graphs

 -- Recommendations --
  If you're not finding helpful recommendations, try searching for one of:
    - computer vision navigation

  (0.343) Multirobot rendezvous with visibility sensors in nonconvex environments http://arxiv.org/abs/cs/0611022v1
  Preview:
    This paper presents a coordination algorithm for mobile autonomous robots. Relying upon distributed sensing the robots achieve rendezvous, that is, th...

  (0.338) Robotics Vision-based Heuristic Reasoning for Underwater Target Tracking
  and Navigation http://arxiv.org/abs/cs/0601064v1
  Preview:
    This paper presents a robotics vision-based heuristic reasoning system for underwater target tracking and navigation. This system is introduced to imp...

  (0.335) Asymptotic constant-factor approximation algorithm for the Traveling
  Salesperson Problem for Dubins' vehicle http://arxiv.org/abs/cs/0603010v1
  Preview:
    This article proposes the first known algorithm that achieves a constant-factor approximation of the minimum length tour for a Dubins' vehicle through...
```

Key parts:
- The initial header shows a preview of the content for easy matching to the current document
- The first recommendation is an "inversion" of the content's embedded concept into the phrase that best matches it, to be used (in the future) for searching for new content
- The remaining recommendations are individual documents presented with a match score, title, a content preview and a link to read more

The current source for this is arXiv, performing a search on a small subset of
the Robotics category of papers.

Out of this, I'm actually interested in the first two links as extensions to
the research direction I'm aiming for while writing about the topic. This
search should also monotonically improve as I add additional documents to the
database.

# Under The Hood

## Search

Search is performed by embedding every paragraph of every document into a
vector search database, along with metadata about a link to the source, a
unique identifier and a title. For the most part, each document is a single
paragraph for the abstract of the paper.

The vector search database takes care of most of the rest. A perk of taking
this approach is that I could also integrate other content sources (such as
Mastodon posts) without having to change this pattern

The downside to this approach in its current implementation is that it rebuilds
the vector database each time the script launches instead of loading it from a
stored file.

## Library Extensions

The vector database is built on the
[vectordb2](https://github.com/kagisearch/vectordb) library by Kagi. I added
additional extensions to the interface (mostly repackaging existing logic) to
allow for embedding content without searching, searching an embedding,
inverting an embedding and finding the distance from an embedding to a topic
(really any string).

## Search Recommendation / Embedding Inversion

To invert embeddings and recover a phrase, all document contents are chunked
into length-3 chunks and put into a separate vector database. The same
embeddings are used, and the closest 3 word phrase to the given embedding is
used as the approximate concept, phrase or text representation for the
embedding. This allows use with encode-only models, at the expense of having to
push a lot more encodings into a sidecar database.

## Shelves

"Today I learned" about the Python built in library `shelves`. It functions as
a dictionary, except that the dictionary concepts are saved (pickled) to a file
to be persisted across script runs. This has allowed me to immediately
implement a "kind" content downloader that stops as soon as it recognizes its
already saved the content instead of querying for it again by persisting saved
records without having to switch mental models to a database.

# Next Steps

- Better saving/storing of the vector database, which will save ~100 seconds for each script invocation and bring the script down to ~20 seconds
- Expanding the database source, ideally to encapsulate a large fraction of the arXiv metadata for relevant topics (robotics, artificial intelligence, machine learning, compilers, symbolic computation, software engineering)
- Running a daily script that can download articles (maybe from the topic RSS feed) as a daily incremental update
- For some documents, it may be helpful to invert the output, so you can show documents that matched multiple chunks of the text, and then which chunks of text were matched instead of having to go chunk by chunk and remember if a document might match multiple areas of interest

# Post Script

While running the tool against this document, I got a few recommendations which
will be interesting topics (if not exactly related to extending this post):

Unmanned Aerial Vehicle Instrumentation for Rapid Aerial Photo System http://arxiv.org/abs/0804.3894v1

Replay Debugging of Complex Real-Time Systems: Experiences from Two Industrial Case Studies http://arxiv.org/abs/cs/0311019v1

Iterative MILP Methods for Vehicle Control Problems http://arxiv.org/abs/cs/0505042v1


