---
Title: Research Areas for 2025
Category: Building
Tags: Research, SSA, EKF, Factor Graph, Drone, Compiler, SSA, SIMD, Practices, Discovery, SLAM, Visual Odometry
Date: 2025-02-11
Updated: 2025-02-11
Summary: I'm focusing on starting 2025 by getting more actively connected to research in a variety of fields for the year.
---

I'm focusing on starting 2025 by getting more actively connected to research in
a variety of fields for the year.

# Topics

## Compilers

- SSA
- SIMD, implicit SIMD

## Drones

- Visual Odometry
- Visual Inertial Odometry
- VI SLAM w/ Factor Graphs

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
