---
Title: random-code Day 4: Littering
Category: Building
Tags: Open Source, random-python, Project Random, testing
Date: 2022-08-02
Updated: 2022-08-07
Summary: How do you test a Transformer and if scoping is working?
---

I got inspired by Zac Hatfield-Dodds's blog post [Sufficiently Advanced
Testing](https://zhd.dev/sufficiently/) to pursue the challenge of construction
random programs. To get the intro of what I've worked on so far check out the
[Day 1 post](blog/starting-the-random-code-journey.html) and the latest [Day 3
post](blog/random-code-day-3.html)

# Schrödinger's cat

The question I've been pondering today is: "How do you test a Transformer and
if scoping is working?"

Scoping is the most important thing I've been focusing on so far with the
project. On one side, you have name discovery to figure out which names we need
to check against the scope. On the other side, you have the book-keeping for
keeping track of which names are in scope at each step in the code.

Testing this logic feels a little bit like Schrödinger's cat. The scope is
almost always changing as the Transformer is visiting different nodes. This
makes it tricky to write  a test to run the Transformer and then inspect if the
scope is correct because the scope can be correct to start, correct at the end,
but incorrect somewhere in the middle of exploring the AST.

## Transformer you say?

NodeTransformer is a pattern for viewing and modifying the AST.

The general pattern is the Visitor, which makes it easy to view data in a tree
structure by "visiting" each node in the tree and calling a specific function
based on its type. This can be applied to lots of tree structures, but is
useful for the AST because we're dealing with many (but well documented) types
of nodes that we might want to view.

Taking it one step more specific, the Transformer is a Visitor that can help
you swap out the node that you've visited. You can completely change the node
that's in the tree, but for this use case we can stick to the simpler task of
swapping out different instances of the same type of node (e.g. one function
definition for another).

# Solution: Constantly Observe the "Cat"

The solution I've come up to is to put the Transformer's common structure of
visiting and modifying each node to use. At each step of the way, we can
annotate the node with the scope that's available. Afterwards, when observing
the tree in a test, we can check each node and use that to understand if it's
working properly. To stretch the Schrödinger's cat analogy one last time, we
want to repeatedly observe the "cat" so we know its state.


