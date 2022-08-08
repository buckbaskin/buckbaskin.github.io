---
Title: random-code Day 4: Littering
Category: Building
Tags: Open Source, random-python, Project Random, testing
Date: 2022-08-02
Updated: 2022-08-07
Summary: How do you test a Transformer and if scoping is working?
---

I got inspired by Zac Hatfield-Dodds's blog post [Sufficiently Advanced
Testing](https://zhd.dev/sufficiently/) to pursue the challenge of construction
random programs. To get the intro of what I've worked on so far check out the
[Day 1 post](blog/starting-the-random-code-journey.html) and the latest [Day 3
post](blog/random-code-day-3-testing.html). Check out the
[random-python](https://github.com/buckbaskin/random-python) project on
Github.

# Schrödinger's cat

The question I've been pondering today is: "How do you test a Transformer and
if scoping is working?"

Scoping is the most important thing I've been focusing on so far with the
project. On one side, you have name discovery to figure out which names we need
to check against the scope. On the other side, you have the book-keeping for
keeping track of which names are in scope at each step in the code.

Testing this logic feels a little bit like Schrödinger's cat. The scope is
almost always changing as the Transformer is visiting different nodes. This
makes it tricky to write  a test to run the Transformer and then inspect if the
scope is correct because the scope can be correct to start, correct at the end,
but incorrect somewhere in the middle of exploring the AST.

## Transformer you say?

[NodeTransformer](https://docs.python.org/3.8/library/ast.html#ast.NodeTransformer)
is a pattern for viewing and modifying the AST.

The general pattern is the
[Visitor](https://docs.python.org/3.8/library/ast.html#ast.NodeVisitor), which
makes it easy to view data in a tree structure by "visiting" each node in the
tree and calling a specific function based on its type. This can be applied to
lots of tree structures, but is useful for the AST because we're dealing with
many (but well documented) types of nodes that we might want to view.

Taking it one step more specific, the Transformer is a Visitor that can help
you swap out the node that you've visited. You can completely change the node
that's in the tree, but for this use case we can stick to the simpler task of
swapping out different instances of the same type of node (e.g. one function
definition for another).

# Solution: Constantly Observe the "Cat"

The solution I've come up to is to put the Transformer's common structure of
visiting and modifying each node to use. At each step of the way, we can
annotate the node with the scope that's available. I call this process littering.
Afterwards, when observing the tree in a test, we can check each node and use
that to understand if it's working properly. To stretch the Schrödinger's cat
analogy one last time, we want to repeatedly observe the "cat" so we know its
state.

Specifically for the random-python project, each AST node that gets processed
(excepting strings) gets tagged with a new property `_ending_scope` and a copy
of the scope is assigned. This is useful for asserting both that certain names
are in scope (e.g. the name of a function is in scope in its body for recursive
calls) and for asserting a name is not in scope (e.g. a local variable defined
in a function definition body isn't present in the code after the function
definition).

## Testing with Littering

Testing with littering enabled are fairly straightforward. In about 10 lines of
code, we set up a small Python snippet with the relevant AST node, parse it to
the AST, then run it through the transformer. We can then assert on the scope.
The
[tests](https://github.com/buckbaskin/random-python/blob/b4a9d4d3c5307d34e4504efaedf58ff52bf2b0c0/test/scoping_test.py#L35-L47)
look something like this:

    def test_FunctionDef_annotation():
        input_text = """
    def main(i: i):
        return 1
    """
        ast = str_to_ast(input_text)
        transformer = build_transformer(ast)
        result = transformer.visit(ast)
    
        assert isinstance(result, FunctionDef)
        args = result.args
        assert isinstance(args, arguments)
        assert "i" not in args._ending_scope

## Easy Littering

Remembering to assign these scopes in all of the relevant places can be easy to
forget for functions with multiple returns or otherwise require copying around
a lot of code. To make the littering process easier, the project defines a
[`littering`](https://github.com/buckbaskin/random-python/blob/b4a9d4d3c5307d34e4504efaedf58ff52bf2b0c0/random_code/impl.py#L744-L760)
decorator that takes in the name of the variable its copying and the variable
its writing to. The decorator calls into the main function, but after the main
function returns and before the decorator returns it performs an assignment to
"litter" the AST node being returned. This ensures that regardless of how the
function exits we'll always get the littering for existing code and as I add
new functionality.

A secondary benefit of moving to the decorator is that I had to standardize the
interface to the visitor functions. Previously, I'd mixed functions that looked
like free functions (no self) with functions that looked like member functions
(that included self) and now they're all standardized as functions, both
hand-written and generated, that accept self as members of the class.

# Conclusion

All together, we've been able to go from uncertainty about scopes to easily
writing tests for scoping by applying littering. This implementation pattern
makes it easier to expand tests with simple or complicated examples and the
decorator makes it easy to ensure that we get the same behavior across the AST
as we add functionality.
