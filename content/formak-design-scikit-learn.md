---
Title: FormaK Coming Soon: Scikt-Learn Integration
Category: Building
Tags: FormaK, 30 for 30, Python, Scikit-Learn
Date: 2022-10-06
Updated: 2022-10-02
Summary: There's a new feature coming to Formak: integration with sckit-learn. This enables quickly integrating new features such as model selection, pipelines and other data tooling.
---

# Overview

FormaK aims to combine symbolic modeling for fast, efficient system modelling
with code generation to create performant code that is easy to use.

The values (in order) are:

- Easy to use
- Performant

The Five Key Elements the library provides to achieve this (see parent) are:

1. Python Interface to define models
2. Python implementation of the model and supporting tooling
3. Integration to scikit-learn to leverage the model selection and parameter tuning functions
4. C++ and Python to C++ interoperability for performance
5. C++ interfaces to support a variety of model uses

This design provides the initial implementation of third of the Five Keys
"Integration to scikit-learn to leverage the model selection and parameter
tuning functions". Scikit-learn is a common library who's interface is
replicated many places (e.g. dask-ml for scaling up machine learning tasks)
that's a good place to start with for an easy to use library.

Why is scikit-learn and machine learning relevant? Conceptually, a detailed,
physical model derived from first principles describes both one complex model,
as well as a space of models derived via simplifications, enhancements or even
disconnected approximations from the original model. Using data from the system
we hope to describe, we can select the appropriate model from the space. This
process is very analogous to a machine learning model, where we have one idea
of how to approximate the system and want to select machine learning models (in
a more algorithmic sense of the term models) and their parameters to best fit
data.

# The Dream

In the end, my hope is that the user can provide an arbitrarily complex
description of the system as a model and provide data and auto-magically get a
best fit approximation to their system. Providing a more complicated model
provides more of a space for discovering improvements to the final system in
the same way providing more data can improve the final system. The "auto-magic"
doesn't come from anything magical; instead, it comes from accumulating
knowledge and how to use it in one place where the final level (improved
knowledge) can also improve the final system above and beyond that which could
be achieved by the user alone. Scikit-learn makes some of this process easier,
especially when it comes to comparing multiple candidate models.


# What could this look like?

Scikit-learn offers helpful tooling for many things, including model selection,
cross validation and building pipelines from estimators and transformers.
By borrowing from scikit-learn's [Pipeline
documentation](https://scikit-learn.org/stable/modules/compose.html#pipeline)
and [Model Selection
documentation](https://scikit-learn.org/stable/modules/cross_validation.html)
we can build the code to compose a pipeline and validate the estimator:

    from formak import py
    
    from sklearn.decomposition import PCA
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    
    formak_model = py.Model(...)
    
    estimators = [('reduce_dim', PCA()), ('formak model', formak_model)]
    pipeline = Pipeline(estimators)
    
    # ... load some data X, y...
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    
    pipeline.fit(X_train, y_train)
    
    pipeline.score(X_test, y_test)

This is just a small part of what scikit-learn has to offer. For example,
scikit-learn has additional functionality for [detecting
outliers](https://scikit-learn.org/stable/modules/outlier_detection.html) and
other [unsupervised
learning](https://scikit-learn.org/stable/unsupervised_learning.html)
capabilities that are direclty useful to FormaK.
