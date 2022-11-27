---
Title: SIMD and Graphs: Partitioning Graphs into data-dependency levels
Category: Building
Tags: Miniseries, FormaK, Graphs, SIMD
Date: 2022-11-26
Updated: 2022-11-27
Summary: This post is a new episode in a miniseries focused on SIMD instructions. This second post focuses on fusing common single operations across multiple data
Image: img/compute-graph-matching.jpg
---

This post is a new episode in a miniseries focused on SIMD
instructions. This post focuses on fusing common single operations
across multiple data. If you haven't read the first post, I recommend reading
the [first post](/blog/simd-and-graphs-graph-matching.html) on graph matching
first.
1. [Parse the sympy graph into a subset of pattern matches with partial orderings of patterns that contain (depend upon) other patterns](/blog/simd-and-graphs-graph-matching.html)
2. Perform common subexpression elimination to deduplicate computations
3. Run the Coffman-Graham algorithm to get a bounded nearly optimal allocation of the matches (This post)
4. Edit the SIMD compute node in place of matching patterns

SIMD (Single Instruction Multiple Data) looks to speed up performing the same
calculation across multiple sets of data. Now that we have operations that
match the SIMD operation, how do we know which nodes in the graph we can
combine? We need to respect data dependencies to make sure that we don't try
to do two operations that depend on each other or perform a computation before
its inputs are ready.

Skip to [a solution](#a-solution)

# Missteps

A brief note on the missteps: These are avenues that I didn't explore or bugs
that I ran across. While not immediately helpful, they may form a bridge to
future ideas in the series.

## A bug when it comes to matching

If the matching provided by the end user is too strict, it can result in an
empty set of "ordered nodes". From there, there is no ordering between the
following nodes added to the list. The symptom of this is to add nodes to levels
in the wrong order and miss dependencies. The easiest place to check for this is
at the end of the setup by asserting that there are ordered nodes before trying
to add in nodes with dependencies. This was tricky to find because it originally
showed up in a way that made it look like the dependency checking was not
working.

## Graph uniqueness

The algorithm currently doesn't interface well with common subexpression
elimination. This would lead to nodes being referred to through multiple paths
in the graph and cause the node identification via path to break down.

## Crossover between SIMD operations

This algorithm focuses on introducing operations for a single type of SIMD
operation. Further design will be needed for choosing between multiple
operations. For example, some SIMD operations perform an add and multiply and
different SIMD operations operate at different precisions.

# A Solution

[Github PR](https://github.com/buckbaskin/formak/pull/6/files)

The algorithm of choice for this kind of bundling is the
[Coffman-Graham](https://mathweb.ucsd.edu/~ronspubs/72_04_two_processors.pdf)
algorithm. It's original intent is to schedule minimal-length schedules across
multiple processors for a known finite number of processors; however, we can
bend it slightly to adapt it to SIMD algorithms where we have multiple processor
lanes as long as the data is independent. Even better, the algorithm is
demonstrated to be optimal.

## The Algorithm

The Coffman-Graham algorithm breaks down into two phases:
1. Topological Sort
2. Leveling

### Topological Sort

In the first phase, nodes in the compute graph are ordered based on their dependencies
(topological sort) with a special lexicographical ordering: Take nodes that had
their dependencies recently added to the sorted ordering before nodes with less
recent dependencies. Intuitively, this has the effect of performing a
depth-first ordering of the data dependencies to order longer chains earlier and
bundle together chains of dependencies.

    ordered_nodes, unordered_nodes = setup_coffman_graham(graph, matcher)
    assert len(ordered_nodes) > 0

    def coffman_graham_filter_criteria(node):
        path_to_expr, expr = node

        for idx in range(len(expr.args)):
            if tuple(path_to_expr + (idx,)) in unordered_nodes:
                # Don't try to insert nodes that depend on unordered nodes
                return False

        # Node only depends on ordered nodes
        return True

    def coffman_graham_sort_criteria(node):
        path_to_expr, expr = node
        args_depth_from_end = []

        for arg_idx, arg in enumerate(expr.args):
            arg_path = path_to_expr + (arg_idx,)
            for ordered_idx, (ordered_path, ordered_expr) in enumerate(
                reversed(ordered_nodes)
            ):
                if arg_path == ordered_path:
                    args_depth_from_end.append(ordered_idx)
                    break

        return sorted(args_depth_from_end)

    while len(unordered_nodes) > 0:
        next_in_order = min(
            filter(coffman_graham_filter_criteria, unordered_nodes.items()),
            key=coffman_graham_sort_criteria,
        )
        path, _expr = next_in_order

        ordered_nodes.append(next_in_order)
        del unordered_nodes[tuple(path)]

### Leveling

In the second phase, nodes are processed in the reversed order from the first
phase. Nodes are assigned to the lowest possible level that is at least one
level above their downstream dependencies. The ordering of the first phase leads
us to the smallest possible level stack (the minimal-length schedule). This is
modified slightly to bump dependencies to the next level if the level is full.

    levels = []

    for idx, node in enumerate(reversed(ordered_nodes)):
        min_level = -1
        for inv_level_idx, level in enumerate(reversed(levels)):
            for maybe_dependency in level:
                if is_dependency_of(node, maybe_dependency):
                    min_level = len(levels) - inv_level_idx - 1
                    # need to go to a greater level
                    break
            if min_level > -1:
                break

        for level_idx in range(min_level + 1, len(levels)):
            if len(levels[level_idx]) < width:
                levels[level_idx].append(node)
                break
        else:
            # We didn't find an acceptable level, so put it at a new higher level
            levels.append([node])

    return levels

## FilterVisitor Pattern

This solution leans on the visitor pattern and matching structure from the
previous post to set up the problem, which I'll refer to as the FilterVisitor.

To start the topological sort, we want to create an
ordered list of nodes with no dependencies (leaves, usually symbols and
constants) and an unordered map. By visiting the tree and matching our target
operations, we can push them into the set of unordered operations and push the
leaves into the ordered list.

    def visit_sympy_expr(expr, matcher, base=None):
        if base is None:
            base = tuple()

        if matcher(expr):
            yield base, expr

        for idx, arg in enumerate(expr.args):
            for result in visit_sympy_expr(arg, matcher, base + (idx,)):
                yield result

The matcher used for this example is:

    def match_Add(expr):
        return expr.func == sympy.core.add.Add or len(expr.args) == 0

## Related Work

### LLVM

LLVM's [auto-vectorization](https://www.llvm.org/docs/Vectorizers.html)
focuses on two use cases:
1. Loops
2. superword-level parallelism aka "SLP"

The loop vectorizer case is straightforward: process multiple iterations of a loop
in parallel. The use case I'm covering is closer to the SLP case:

> combine similar independent instructions into vector instructions

and

> The SLP-vectorizer processes the code bottom-up, across basic blocks, in
> search of scalars to combine.

According to benchmarks by 
[Michael Larabel](https://www.phoronix.com/news/MTQyMzQ) from an old version of
LLVM (circa 2013), the SLP vectorization isn't as impactful as the loop
vectorizer.

### Research into Superword Level Parallelism

[This page](https://groups.csail.mit.edu/cag/slp/) references three papers for
integrating superword-level parallelism into compilers (circa 2000). For
example, [this paper](https://groups.csail.mit.edu/cag/slp/SLP-PLDI-2000.pdf)
and a follow up 
[project to implement it in LLVM](https://15745-slp-project.github.io/Final.pdf)
suggest that performance improvements can be gained by being smart about
additional optimization combinations applying SLP that goes beyond what the LLVM
compiler achieves today.
