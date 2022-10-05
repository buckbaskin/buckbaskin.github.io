---
Title: 30 for 30: Open Sourcing "FormaK"
Category: Building
Tags: Open Source, Software Engineering, 30 for 30, FormaK, Project FormaK
Date: 2022-10-01
Updated: 2022-10-01
Summary: Starting live development of a new open source project
---

This October, I'm committing to committing to the FormaK project every day and writing a
blog post about development and adjacent projects that I'm working on.

# The FormaK Project

What is the FormaK project do you ask? The FormaK project aims to combine symbolic 
modeling for fast, efficient system modeling with code generation to create performant
code that is easy to use.

## A Simple Model

With a little simplification, a
[model](https://github.com/buckbaskin/formak/blob/master/featuretests/python_ui_demo/simple_test.py)
that looks like this:

```python
    dt = Symbol("dt")

    tp = trajectory_properties = {k: Symbol(k) for k in ["mass", "z", "v", "a"]}

    thrust = Symbol("thrust")

    state = set(tp.values())
    control = set([thrust])

    state_model = {
        tp["mass"]: tp["mass"],
        tp["z"]: tp["z"] + dt * tp["v"],
        tp["v"]: tp["v"] + dt * tp["a"],
        tp["a"]: -9.81 * tp["mass"] + thrust,
    }

    model = Model(dt=dt, state=state, control=control, state_model=state_model)
```

## Useable C++

... becomes code you can use that looks like this:

`generated/simple.h`
```c++
class StateModel {
    State process(const State& state, const Control& control);
    // implementation also generated
};
```

If you'd like to see examples that are beyond a toy example, check out the project 
[demos](https://github.com/buckbaskin/formak/tree/master/demo/src).

# 30 for 30

My goal is to work on consistently contributing to the project and writing about it. To that
end, I'm going to be writing and posting here once daily about what I'm working on and what
I'm learning about to advance the project.

# Learn More

The FormaK project is hosted at [github.com/buckbaskin/formak](https://github.com/buckbaskin/formak) 

To get started with the project, check out the [documentation](https://github.com/buckbaskin/formak/blob/master/docs/getting-started.md)

To learn about the future of the project, check out the [design doc](https://github.com/buckbaskin/formak/blob/master/designs/formak_v0.md).

For more posts in the series, check out the tag [30 for 30](buckbaskin.com/blog/tag/30-for-30.html) and tag [FormaK](buck.baskin/blog/tag/foramk.html) for ongoing updates about the project.
