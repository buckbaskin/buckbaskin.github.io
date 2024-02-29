---
Title: Superoptimization - New FormaK Experiment
Category: Building
Tags: FormaK, Project FormaK, Python, Code Generation
Date: 2024-02-28
Updated: 2024-02-28
Image: img/FstyleK.jpg
Summary: A new experiment for FormaK has landed: Superoptimization. Instead of individual peephole optimization, the experiment prototypes using search and a model of the CPU to find the optimal ordering of all operations.
---

## Overview

FormaK aims to combine symbolic modeling for fast,
efficient system modelling with code generation to create performant
code that is easy to use.

The Five Key Elements the library provides to achieve this user experience are:

1. Python Interface to define models
2. Python implementation of the model and supporting tooling
3. Integration to scikit-learn to leverage the model selection and parameter tuning functions
4. C++ and Python to C++ interoperability for performance
5. C++ interfaces to support a variety of model uses

This design focuses on experimenting with the possible performance benefits
from the straightforward (common subexpression elimination) to the magical:
super-optimization.

The performance is relevant in two key ways:

1. Evaluating the runtime of the output program vs the current system
2. Evaluating the compile time of the super-optimizing program to see if it is sufficiently fast to be usable

This design is experimental in nature, so the end goal is only to collect this
data to establish a data point from which future work can proceed. There is no
goal to have this design be a full feature of the project.

### Superoptimization

[Superoptimization](https://en.wikipedia.org/wiki/Superoptimization) is the
process of searching to find the optimal code sequence to compute a function.

For this design, the approach will be to perform a search on the compute graph
to find the sequence of operations that lead to the fastest possible
computation. To do that search, a CPU model will be used to allow for mapping
operations to a more detailed sense of time (vs assigning each operation a
fixed time), primarily focusing on modeling memory latency and CPU instruction
pipelining. This will allow the search to model the state of the CPU at each
instruction and have a better approximation of the total time to compute the
sequence.

## Solution Approach

### Search

By taking a graph-based approach, the search algorithm `A*` (A-star) can be
used to speed up the search with heuristics. The key to using `A*` search
effectively is a heuristic that is quick to compute, admissible and consistent.

[Admissible](https://en.wikipedia.org/wiki/Admissible_heuristic)

> a heuristic function is said to be **admissible** if it never overestimates
> the cost of reaching the goal, i.e. the cost it estimates to reach the goal
> is not higher than the lowest possible cost from the current point in the
> path

[Consistent](https://en.wikipedia.org/wiki/Consistent_heuristic)

> a heuristic function is said to be **consistent**, …  if its estimate is
> always less than or equal to the estimated distance from any neighboring
> vertex to the goal, plus the cost of reaching that neighbor.

The quick to compute part is relevant because the end to end search time could
end up being slower if it’s faster to evaluate some large portion of the graph
than to evaluate the heuristic function. In this case, given that the CPU model
may grow to be somewhat complex, the heuristic should have a low hurdle to step
over (or a high ceiling to step under?).

### CPU Model

The CPU model used in this superoptimization will focus on a few key features
of CPUs: pipelining of independent operations and memory load latency. This
focus comes because the modeling of these two effects is approximately
tractable and the two effects should have a straightforward implications for
the output graph:

- If you can change the order of two compute operations so more are running in parallel via pipelining than the overall compute will be faster.
- If you can load some memory earlier, than later computations may not need to wait as long

For kicks, they’re also parts of the CPU I’m interested in modeling.

Pull Request: [#26](https://github.com/buckbaskin/formak/pull/26)
Commit: [42b0e0c](https://github.com/buckbaskin/formak/commit/42b0e0c1279f6f2435faf672bf9b2051043f01dc)

# Why?

Superoptimization is an exciting compiler process that can lead to significant
performance improvements not available any other way; however, it's
implementation is decidedly... "not trivial". Given that, I opted to make this
a time-bounded experiment where I could explore the concept, practice
implementing a neat and tidy algorithm (`A*` search) and maybe unlock
optimizations for the future of the project.

In the end, I ran into issues where the required searching may outstrip my
patience for waiting to see if the algorithm worked, but I do think the
approach has promise.

Getting started for the year with a fixed time task also made it easy to start
the year with a definite contribution. I ended the year with a feature that
dragged on for a while, so going to the opposite approach was appealing.

# What's next?

The next feature will be implementing some portion of the [netcode
enhancement](https://github.com/buckbaskin/formak/issues/24), but that's still
to-be-determined.
