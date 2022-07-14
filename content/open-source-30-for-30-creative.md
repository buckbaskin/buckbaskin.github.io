---
Title: 30 for 30: Open Source "Creative"
Category: Building
Status: Draft
Tags: Open Source, Software Engineering, 30 for 30, Creative
Date: 2022-10-01
Updated: 2022-07-13
Summary: Starting live development of a new open source project
---

This October, I'm committing to committing to the Creative project every day and writing a
blog post about development and adjacent projects that I'm working on.

# The Creative Project

What is the Creative project do you ask? The Creative project aims to combine symbolic 
modeling for fast, efficient system modeling with code generation to create performant
code that is easy to use.

## A Simple Model

With a little simplification, a model that looks like this:

```python
    vp = vehicle_properties = {k: Symbol(k) for k in ["x", "y", "theta"]}
    state = set([vp["x"], vp["y"]])
    control = set([vp["theta"]])

    state_model = {
        vp["x"]: vp["x"] + cos(vp["theta"]),
        vp["y"]: vp["y"] + sin(vp["theta"]),
    }

    # Optional
    initial_state = {
        vp["x"]: 0.0,
        vp["y"]: 0.0,
        vp["theta"]: 0.1 * pi,
    }
```

## Useable C++

... becomes code you can use that looks like this:

`generated/simple.h`
```c++
class Example {
   int i;
};
```

<!-- TODO(buck) demo codegen -->

If you'd like to see examples that are beyond a toy example, check out the project 
[demos](https://github.com/buckbaskin/creative/tree/master/demo).

# 30 for 30

My goal is to work on consistently contributing to the project and writing about it. To that
end, I'm going to be writing and posting here once daily about what I'm working on and what
I'm learning about to advance the project.

<!-- TODO(buck) better image -->

![Image]({attach}/img/IMG_0671.jpg)

# Learn More

The Creative project is hosted at [github.com/buckbaskin/creative](https://github.com/buckbaskin/creative) 

To get started with the project, check out the [documentation](https://github.com/buckbaskin/creative/blob/master/docs/getting-started.md)

To learn about the future of the project, check out the [design doc](https://github.com/buckbaskin/creative/blob/master/designs/creative_v0.md).

For more posts in the series, check out the tag [Creative](buckbaskin.com/blog/tag/macro.html)
