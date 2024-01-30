---
Title: Hyperparameter Selection - New FormaK Feature
Category: Building
Tags: FormaK, Project FormaK, Python, C++, Kalman Filter, scikit-learn
Date: 2024-01-30
Updated: 2024-01-30
Image: img/FstyleK.jpg
Summary: A new feature for FormaK has landed: Hyperparameter selection. Automatically select optimal parameters based on data from the modeled system.
---

FormaK aims to combine symbolic modeling for fast, efficient system modelling
with code generation to create performant code that is easy to use.

This design focuses on "Integration to scikit-learn to leverage the model
selection and parameter tuning functions". More specifically, this design
focuses on using scikit-learn tooling to automatically select the innovation
filtering level from data.

The promise of this design is that all parameters could be selected
automatically based on data instead of requiring hand tuning; however, this
design will focus narrowly on selecting the innovation filtering level as a
motivating example.

Pull Request: [#21](https://github.com/buckbaskin/formak/pull/21)
Commit: [5ce60af](https://github.com/buckbaskin/formak/commit/5ce60afe2bc82c04d99de3b87fde2c9a72256411)

# Why?

The Kalman Filter has a number of selectable parameters:
- process noise for each reading of the state vector
- sensor noise for each element of the reading vector

The
[innovation filtering
approach]({filename}formak-feature-innovation-filtering.md) also introduces an
additional parameter and future designs will likely introduce additional
parameters as well.

This could be treated as a magic number or a human-tuned parameter; however,
machine learning provides a better process: [cross
validation](https://scikit-learn.org/stable/modules/grid_search.html).

Given data and a measure of fit (innovation), we can select different sets of
parameters based on training data, validate it against other training data and
cross-validate it against a held-out test set. This means that data can point
us to the correct parameters for the filter and the cross validation approach
should reduce the risk of overfitting.

All of this is of some complexity to set up and get running, so integrating it
into FormaK will allow for easily expanding its use and re-use in my own work,
sharing the process with other people without having to re-implement the
process.

# What's next?

As a next step, I'm opening up the roadmap for FormaK via [Github
Issues](https://github.com/buckbaskin/formak/issues). For each proposal, I'm
outlining the overview of the concept, how it fits into the FormaK project
goals, design decisions that will need to be made and seeking feedback.

After getting that part of the project set up, I'll move onto the next feature.
I suspect the next feature will be implementing some portion of the [netcode
enhancement](https://github.com/buckbaskin/formak/issues/24), but that's still
to-be-determined.
