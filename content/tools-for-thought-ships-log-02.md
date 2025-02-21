---
Title: Tools for thought - Ship's Log 2
Category: Building
Tags: Research, Practices, Discovery
Date: 2025-02-19
Updated: 2025-02-21
Summary: Building on the learnings from last time, I'm working on speedups to significantly reduce the time to launch the interactive features to make them more, well, interactive. Previously, the script was taking 800 seconds! on startup and that has been improved significantly.
---

Building on the learnings from 
[last time]({filename}/tools-for-thought-ships-log-01.md), I'm working on
speedups to significantly reduce the time to launch the interactive features to
make them more, well, interactive. Previously, the script was taking 800
seconds (800!) on startup and that has been improved significantly.

# Speed - Part 2
[Part 1]({filename}/tools-for-thought-ships-log-01.md#speed)

Previously...

> The latest run with an expanded search area led to an almost 800 second
database creation time (for ~800 documents). This essentially turns an
"interactive" script into a batch script, which defeats the purpose of being
able to use it while thinking and writing.
>
> I think I can achieve this level of interactivity (say less than 1 minute from
save to recommendations) by saving the vector database locally and then
updating it incrementally at download time

... And the results (with the same documents, and 39 recommendations)

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
seconds of loading them from a local file. A worthwhile trade

The new longest pole in the experience is the recommendations; however, these
are done in an incremental approach with the current UI, so the user can still
get some value before the 70 seconds of recommendations are complete.

# Easier downloads scripting - Part 2
[Part 1]({filename}/tools-for-thought-ships-log-01.md#easier-downloads-scripting)

As I'm writing, I've identified topic areas where I'm getting no matches (in
this case, camera intrinsics and online estimation of said camera intrinsics).
I'd like to be able to do something like

    python keyword_search.py "online estimation camera intrinsics"

In the same vein, I'd like to be able to gather a broad category

    python category.py "cs:RO"

# Other Notes

## User Interface Idea

I prefix questions I have with "Open Question". I could use this as a key for
paragraphs to generate extra results (say 5 instead of 3) and surface them
independently from the aggregated list of most likely interesting sources. I should also remove the "Open Question" part because that seems to bias the content away from what I'm looking for. A line

     Open question: how feasible is it to estimate camera intrinsics online in a strapdown visual inertial odometry system?

matches to results with poor match scores

     (0.747) Perturbation theory and canonical coordinates in celestial mechanics https://arxiv.org/abs/2209.07457v2
     Preview:
       In this paper, we study in-depth the problem of online self-calibration for robust and accurate visual-inertial state estimation. In particular, we fi...
    
     (0.710) Bridging Zero-shot Object Navigation and Foundation Models through
     Pixel-Guided Navigation Skill https://arxiv.org/abs/2309.10309v2
     Preview:
       This paper presents an online initialization method for bootstrapping the optimization-based monocular visual-inertial odometry (VIO). The method can ...
    
     (0.681) ETPNav: Evolving Topological Planning for Vision-Language Navigation in
     Continuous Environments https://arxiv.org/abs/2304.03047v3
     Preview:
       Visual-inertial navigation systems are powerful in their ability to accurately estimate localization of mobile systems within complex environments tha...



In the same vein, I can probably skip chunks that are just links, until I get
to the point of going and fetching the link contents to use (but this probably
doesn't need to be done for a while)
