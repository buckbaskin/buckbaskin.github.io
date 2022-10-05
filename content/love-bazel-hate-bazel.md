---
Title: I Love Bazel, I Hate Bazel
Category: Building
Tags: Bazel, FormaK, Project FormaK, Selenium, 30 for 30
Date: 2022-10-02
Updated: 2022-10-01
Summary: I love Bazel. It's one of those satisfying tools where computer science algorithms and data structures fuse with good software practice to create something that's satisfying on many levels. It knows how to minimally rebuild things. It knows how to hermetically build things in a repeatable way. I also hate Bazel.
Image: img/bazel-sketch.jpg
---

I love Bazel. It's one of those satisfying tools where computer science
algorithms and data structures fuse with good software practice to create
something that's satisfying on many levels. It knows how to minimally rebuild
things. It knows how to hermetically build things in a repeatable way. It's
existence made [Merkle
trees](https://sluongng.hashnode.dev/bazel-caching-explained-pt-1-how-bazel-works)
make more sense to me.

I hate Bazel. While trying to figure out building a mix of Python and C++, I've
wandered endlessly trying to sort out how to get it working. I dislike the odd
mix of a large amount of documentation and a large amount of documentation that
doesn't explain what I'm hoping to understand. Python in particular is somewhat
inscrutable in that when trying to build a pytest test, it seemed to repeatedly
break the hermeticity I was hoping I had. Its complexity led to me repeatedly
break things that I thought that I'd fixed.  The diff to fix what I thought was
the right system is largely one made of witch incantations over a cauldron made
by dumping an existing project in and skimming stuff off the top that seemed
passable.

So, on that note, thanks to my savior: the Selenium project. I appreciate it as
a testing tool (one which I find enjoyable), but more now as a multi-language
Bazel project (including Python) whose example I can follow. FormaK's build
structure now heavily borrows from Selenium and it's held up to some minor
expansions. With the Selenium-inspired structure (and essentially standing on
the shoulders of Selenium as my build tools "team") I can now proceed forward
with the more FormaK-y aspects of the project:

- The scikit-learn-ification of FormaK to adapt existing machine learning
  tooling - [Design](https://github.com/buckbaskin/formak/blob/sklearn-integration/designs/sklearn-integration.md)
