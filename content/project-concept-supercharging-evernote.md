---
Title: Project Concept: Supercharging Evernote
Category: Building
Tags: Project Supercharging Evernote, Python, Knowledge Base, Evernote, scikit-learn
Date: 2023-01-14
Updated: 2023-01-29
Summary: I'll admit it. I'm a document hoarder. For years I've been collecting and tagging notes in Evernote as I'll read through them to save for later. Can I use that hoarding to learn better?
---

I'll admit it. I'm a document hoarder. For years I've been collecting and
tagging notes in Evernote as I'll read through them to save for later.
Sometimes I'll read carefully the first time, but sometimes I'd do more of a
skim. By ingesting text content into Evernote and performing some tags, I could
easily find information again through the tags (e.g. finding 
[Sufficiently Advanced Testing](https://zhd.dev/sufficiently/) by tags 
"Python" and "Property
Based Testing") or search (e.g. finding papers related to 
[On-Manifold Preintegration for Real-Time Visual-Inertial Odometry](https://rpg.ifi.uzh.ch/docs/TRO16_forster.pdf) by searching
"preintegration"). The tag portion of the system relies a little bit more on me
correctly remembering to include tags and fix extra tags due to typos or mixing
concepts (e.g. Network for computer networks vs Networking for meeting new
people in my career).

I'm hoping to "learn" a few things about the documents to improve how I can use
Evernote:

- Missing Tags: Generate clusters, look for common tags in the cluster and then add tags to the notes in the cluster that are missing the common tags
- Duplicated Notes: Score documents for similarity across bags of words with "cosine similarity". Manually evaluate pairs of documents with top 10th percentile similarity 
- Interesting Concepts Search: Generate clusters, then look at clusters with at least one document tagged with the original idea as collections of common ideas I may have missed when first read through the note.

This idea overlaps nicely with the class of problems under the heading of
document classification and document clustering. Both of these problems can be
approached with a Bag of Words approach and scikit-learn provides an easy to
follow 
[tutorial](https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html) 
that outlines how to take text documents "labeled" by their Usenet group,
cluster them and evaluate the quality of the clusters compared to the labels.
The tutorial focuses on using TF-IDF (Term Freqency - Inverse Document
Frequency) to highlight key words that are important for each document (feature
extraction), clustering by K-means and extracting the key words for each
cluster. With this tutorial approach, I can use it as analogy for what I'm
hoping to achieve, substituting notes for the Usenet messages and using tags as
labels.

All together, I think I can learn new things about the information I've
collected and multiply the value that I get from my notes. The next step is to
actually parse the notes into a format scikit-learn expects, adapt the tutorial
and mine the clusters for insight.

For more posts about the project, check out the
[project page](/blog/tag/project-supercharging-evernote.html).

# Behind the Scenes

1. [Behind the Scenes 2023-01-13](/blog/behind-the-scenes-2023-01-13.html)

