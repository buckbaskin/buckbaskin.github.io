---
Title: Tools for thought - Trip Report 2
Category: Building
Tags: Research, Practices, Discovery
Date: 2025-02-19
Updated: 2025-02-19
Summary: Building on the learnings from last time, I'm working on speedups to significantly reduce the time to launch the interactive features to make them more, well, interactive. Previously, the script was taking 800 seconds! on startup and that has been improved significantly.
---

Building on the learnings from 
[last time]({filename}/tools-for-thought-trip-report-02.md), I'm working on
speedups to significantly reduce the time to launch the interactive features to
make them more, well, interactive. Previously, the script was taking 800
seconds! on startup and that has been improved significantly.

# Speed - Part 2

The latest run with an expanded search area led to an almost 800 second
database creation time (for ~800 documents). This essentially turns an
"interactive" script into a batch script, which defeats the purpose of being
able to use it "inline" while thinking and writing.

I think I can achieve this level of interactivity (say less than 1 minute from
save to recommendations) by saving the vector database locally and then
updating it incrementally at download time...

And the results (with the same documents, and 39 recommendations)

    Times
    Import Time 5.9 sec
    Memory Construction Time 6.1 sec
    Vector Load Time 794.3 sec
    File Read Time 0.0 sec
    File Embed Time 1.3 sec
    Recommendation Time 73.4 sec


When rerunning, the times are:

    Times
    Import Time 6.0 sec
    Memory Construction Time 22.4 sec
    Vector Load Time 0.0 sec
    File Read Time 0.0 sec
    File Embed Time 1.8 sec
    Recommendation Time 70.4 sec

This shows that I've exchanged 800 seconds of saving new vectors for ~20
seconds of loading them from a local file. That seems like a worthwhile trade.

The new longest pole in the experience is the recommendations; however, these
are done in an incremental approach with the current UI, so the user can still
get some value before the 70 seconds of recommendations are complete.
