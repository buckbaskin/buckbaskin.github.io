---
Title: Innovation Filtering - New FormaK Feature
Category: Building
Tags: FormaK, Project FormaK, Python, C++, Kalman Filter
Date: 2023-09-19
Updated: 2023-09-19
Image: img/FstyleK.jpg
Summary: A new feature for FormaK has landed: Innovation filtering. Automatically make Kalman Filters more robust.
---

FormaK aims to combine symbolic modeling for fast, efficient system modelling
with code generation to create performant code that is easy to use.

The new feature provides an extension to the Python and C++ models to
efficiently provide additional error handling capabilities: innovation
filtering (aka innovation editing).

How should the filter measure the errors? The filter can use the
measurement innovation $$\tilde{z} = z_{t} - \hat{z_{t}}$$ where $z_{t}$ is the
measurement, $\hat{z_{t}}$ the predicted reading and $\tilde{z}$ is the
resulting innovation. Given the innovation, the definition of too large can be
calculated from the expected covariance: $$\tilde{z}^{T} S^{-1} \tilde{z} - m >
k \sqrt{2m}$$ where $S$ is the expected covariance of the measurement, $m$ is
the dimension of the measurement vector and $k$ is the editing threshold. If
this inequality is true, then the measurement is "too large" and should be
filtered (edited). [1] [2]

[1] This approach to innovation filtering, referred to as editing in the text,
is adapted from "Advanced Kalman Filtering, Least Squares and Modeling" by
Bruce P. Gibbs (referred to as [1] or AKFLSM)
[2] The notion follows the convention defined in the
[Mathematical Glossary](../mathematical-glossary.md) which itself is based on
"Probabilistic Robotics" by Thrun et al.

This feature originally was intended to be paired with automatic model fitting;
however, that was not to be. I got myself stuck in a large refactoring trying
to make the interface better. Over 3 weeks and 30 hours I made it through but I
came close to giving up on the feature multiple times when I'd get stuck
finding more refactoring I need to do. Beware the forest of refactoring.

Pull Request: [#18](https://github.com/buckbaskin/formak/pull/18)
Commit: [16ba541](https://github.com/buckbaskin/formak/tree/16ba541e799dfe1b289618a7b27ec48847191172)

# What's next?

## Model fitting

I spent a lot of time in the 
[original design document](https://github.com/buckbaskin/formak/blob/16ba541e799dfe1b289618a7b27ec48847191172/docs/designs/innovation_filtering.md)
describing the model selection process. Now that I've moved past the refactor
and onto the next thing, I'm looking forward to implementing the automatic
model selection process.
