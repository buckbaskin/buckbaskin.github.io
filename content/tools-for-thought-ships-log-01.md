---
Title: Tools for thought - Ship's Log 1
Category: Building
Tags: Research, Practices, Discovery
Date: 2025-02-18
Updated: 2025-02-21
Summary: I started with exploring celestial navigation as an initial use case for the tools for thought. My primary takeaways were that the database creation speed really limits the interactive nature of the tool and that the user interface could be improved.
---

I started with exploring 
[celestial navigation](celestial-navigation-for-drones.md) as an initial use
case for the 
[tools for thought]({filename}/tools-for-thought-and-discovery.md). My primary
takeaways were that the database creation speed really limits the interactive
nature of the tool and that the user interface could be improved.

# Speed

The latest run with an expanded search area led to an almost 800 second
database creation time (for ~800 documents). This essentially turns an
"interactive" script into a batch script, which defeats the purpose of being
able to use it "inline" while thinking and writing.

I think I can achieve this level of interactivity (say less than 1 minute from
save to recommendations) by saving the vector database locally and then
updating it incrementally at download time

# Other Improvements

## User Interface

Right now the recommendations are batched per paragraph; however, in practice
I've found that across, say, the first 10 paragraphs, there are actually 3
papers that are relevant to multiple paragraphs and it'd be more helpful to
surface the top papers (with references to which paragraph they're useful for)
instead of having to read through each paragraph and figure out if I'm seeing
the same information again or considering a new paper.

## Markdown parsing

I'd also like to use Markdown parsing to help skip some of the content that's
less likely to be useful (e.g. headers that are more generic such as "The
Math". In the future, if I've integrated context more then I could integrate
the stack up of headers so that it's something like "Celestial Navigation > The
Math" but for now it's just generic content. In the intervening time, the
proposed document-first organization of the user interface would help avoid
this, where content that's relevant to multiple paragraphs would be surfaced
first

## Easier downloads scripting

I'd like to be able to write some sort of fairly minimal download script with
content that is like "all:compilers" and n = 100 results and run it. Right now
it takes modifying an existing script in place that was intended more as a
proof of concept

The downloading friction is secondary because the speed is slow enough that I
feel incentivized to not add additional content except in areas where there are
absolutely no results

## "Staying on topic"

Another approach to staying on topic would be to calculate the distance from
the topic embedding to the paragraph embedding, and skipping those paragraphs
that don't stay within a finite region around the topic. These can be reported
with their distance from the topic at the end (e.g. "The Math" had a distance
of 0.8 and was skipped). This would allow for manual searching of topics that
were accidentally deemed too far away, but limit noise from papers that are 99%
likely to never be useful
