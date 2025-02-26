---
Title: Research Areas for 2025
Category: Building
Tags: Research, SSA, EKF, Factor Graph, Drone, Compiler, SSA, SIMD, Practices, Discovery, SLAM, Visual Odometry, Celestial Navigation
Date: 2025-02-11
Updated: 2025-02-25
Summary: I'm focusing on starting 2025 by getting more actively connected to research in a variety of fields for the year.
---

I'm focusing on starting 2025 by getting more actively connected to research in
a variety of fields for the year.

# Topics

## Compilers

- SSA
- SIMD

I'd also like to see if I can make progress on tooling to improve code
generation that is only intended to implicitly leverage SIMD instead of having
to generate it explicitly. For example, if I can generate 4 independent add
operations and write them in sequence, it should be feasible for 
[Superword-Level Parallelism](https://llvm.org/docs/Vectorizers.html#the-slp-vectorizer)
tooling to match to SIMD if the cost model lines up.


## Drones

- Visual Odometry
- Visual Inertial Odometry
- VI SLAM w/ Factor Graphs

### Celestial Navigation

One topic that I rediscovered because of drones, but originally connected with
because of sailing and history is celestial navigation. Specifically, celestial
navigation for drones made it to Hacker News 
([discussion link](https://news.ycombinator.com/item?id=42767797)), and I quite
enjoyed reading the paper ([DOI](https://doi.org/10.3390/drones8110652), open
access via the MDPI journal). It sparked some new ideas for me and generally
renewed my interest in learning celestial navigation as a skill

### Underwater Autonomy

An additional topic area that I see as logically adjacent to drones is
underwater autonomous vehicles. Once I've taken some time to explore through
the visual odometry for flying drones, I'd also like to spend some time
exploring similar challenges for underwater vehicles.

# Learning Practices

The research is also taking something of an applied turn, in that in order to
maximize my understanding, I'm aiming to implement more of the papers as I go
instead of just passively consuming them. I see this as a proxy for
understanding, in that if I can't "explain" the paper to a computer, I probably
don't understand the algorithm well enough.

# Discovery

I'm also trying to refine how I discover papers to maximize my reading for what
I'm most likely to find interesting, enjoyable and tractable. In a previous
attempt, I'd used an interactive rating system to recommend arXiv papers;
however, it didn't allow me to easily revisit papers that I had read to upgrade
or downgrade them. I'm actually starting to think that an interface more like a
spreadsheet could help me side-step the interactivity and storage portion, and
then I can build the recommender system as a batch processing.

As a short addendum, the previous approach that I had taken focused on TF-IDF as
a measure of interesting terms and then doing a search that way. In the
going-forward mode, I'd like to explore with using sentence or paragraph
embeddings (e.g. [BERT](https://www.sbert.net/),
[sentence-transformers](https://pypi.org/project/sentence-transformers/) ), and
some combination. For example, given papers that I've read and found interesting
enough to implement, find me papers that match as well as invert the embeddings
to find a three word (or similar short description) of a topic area. I'd also
like to be able to do topic search.
