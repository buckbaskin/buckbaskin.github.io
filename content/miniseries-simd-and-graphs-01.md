---
Title: SIMD and Graphs: Graph Matching
Category: Building
Tags: Miniseries, FormaK, Graphs, SIMD
Date: 2022-11-25
Updated: 2022-11-27
Summary: This post is a new episode in a miniseries focused on SIMD instructions. This first post focuses on matching points in the compute graph where we can combine individual instructions to form SIMD instructions.
Image: img/compute-graph-matching.jpg
---

This post is a new episode in a miniseries focused on SIMD instructions. This
first post focuses on matching points in the compute graph where we can combine
individual instructions to form SIMD instructions.

SIMD (Single Instruction Multiple Data) looks to speed up performing the same
calculation across multiple sets of data. If we can lay out a compute graph of
the operations we want to perform, we can then try and match across operations
with different data (but the same operation) to replace them with the SIMD
operations. SIMD instructions often have 4 or more data paths that run
simultaneously, so if we can successfully match the operations we can get a 4x
speed up in the code.

This miniseries will focus on the steps to go from a symbolic compute graph of
individual operations to a compute graph of SIMD operations. The steps are
broken down into the following:

1. Parse the sympy graph into a subset of pattern matches with partial orderings of patterns that contain (depend upon) other patterns. (This post)
2. Perform common subexpression elimination to deduplicate computations
3. [Run the Coffman-Graham algorithm to get a bounded nearly optimal allocation of the matches](/blog/simd-and-graphs-partitioning-graphs-into-data-dependency-levels.html)
4. Edit the SIMD compute node in place of matching patterns

This post focuses on pattern matching. 

Skip to [a solution](#a-solution)

# Missteps

One of the first thoughts that I pursued was a regex like pattern for specifying
patterns within the graph. The brief intuition is that regex describes finite
state machines and we could use finite state machines to match the graph. The
primary problem I found here was in two parts. First, the language to describe a
match of something like `Add(.*,.*)` didn't scale to matching across graph
levels. Second, it would take some effort to elegantly split an implementation
of regex from its usual linear form to a tree form.

The other misstep to highlight was trying to rewrite a Sympy compute graph into
essentially the same thing with bespoke classes. The outcome of this would have
been the same, with less functionality and harder to integrate out as a second
form of internal representation.

    Add = namedtuple("Add", ["left", "right"])
    # vs
    sympy.core.add.Add

# A Solution

## The Visitor Pattern

After exploring many patterns, the outcome I found most satisfying was that of
the Visitor. It's used in the Python 
[AST library](https://docs.python.org/3/library/ast.html#ast.NodeVisitor).  

> A node visitor base class that walks the abstract syntax tree and calls a
> visitor function for every node found.

Taking this to the Sympy tree with pattern matching in mind, we can visit each
node in the tree and call the matching function. This allows for an easy way to
match whichever function we'd like and provide flexibility for the user. For
example, for the SIMD function `_mm_add_ps` we want to match up to 4 add
operations, so the logic for matching is a simple 
`expr.func == sympy.core.add.Add`.

    def visit_sympy_expr(expr, matcher):
        if matcher(expr):
            yield base, expr
    
        for idx, arg in enumerate(expr.args):
            for result in visit_sympy_expr(arg, matcher):
                yield result

## Prefix

The next element to note about this particular implementation of matching is
that it follows a prefix order. This means that each node will be matched before
each of its children. This doesn't have much significance yet because we're not
manipulating the graph, but it may make other transforms easier later. Consider
it more of a note of an intentional design to revisit later.

    def visit_sympy_expr(expr, matcher):
        if matcher(expr): # prefix
            yield base, expr
    
        for idx, arg in enumerate(expr.args):
            for result in visit_sympy_expr(arg, matcher):
                yield result

        if matcher(expr): # postfix
            yield base, expr
    

## Naming and a Sub-Graph

The final element to note is one of naming. When performing these graph
manipulations it's often useful to have a unique identifier. A typical option
would be a universally unique identifier (UUID) but instead I went with a more
structural approach. For each node, track a list of integers identifying the
heritage. When visiting the child of each node, add the index of the child in
the parents list of arguments to the operator. In this way, each child is
uniquely identified from its siblings (by different indices) and each child is
uniquely identified from its parent (by different length of the list).

    def visit_sympy_expr(expr, matcher, base=None):
        if base is None:
            base = []
    
        if matcher(expr):
            yield base, expr
    
        for idx, arg in enumerate(expr.args):
            for result in visit_sympy_expr(arg, matcher, base + [idx]):
                yield result

This form of unique identifier also allows us to build a sub-graph of the
original nodes in the form of matches. Edges in this graph form simplified data
dependencies across matches and we can identify if there are data depedencies
between matches if one of the identifiers for the node is a prefix to the other.
This is important because SIMD operations are performed in parallel on
independent data, so to form a SIMD node we need to combine nodes without data
dependencies. I'll leave it with that and more to come in the next post in the
miniseries.
