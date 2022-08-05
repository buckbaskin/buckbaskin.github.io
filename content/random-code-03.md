---
Title: random-code Day 3 - Testing
Category: Building
Tags: Open Source, random-python, Project Random, testing, logging
Date: 2022-07-31
Updated: 2022-08-04
Summary: Starting testing and immediately finding some bugs
---

I got inspired by Zac Hatfield-Dodds's blog post [Sufficiently Advanced
Testing](https://zhd.dev/sufficiently/) to pursue the challenge of construction
random programs. To get the intro of what I've worked on so far check out the
[Day 1 post](blog/starting-the-random-code-journey.html) and the latest [Day 2
post](blog/random-code-day-2.html)

# Testing

Testing is made pretty easy with pytest. In a few [lines of
code](https://github.com/buckbaskin/random-python/blob/254e5cbc2f01b3ddddeb5b57c79cb1b5aa829b63/test/name_discovery_test.py#L123-L126),
we can make a little bit of Python, convert it to an AST, make sure we're
working on the correct node and make sure we've discovered the right names with
something like this:

    def test_IfExp():
        ast = _strip_expr(str_to_ast("""0 if name else 1"""))
        assert isinstance(ast, IfExp)
        assert ["name"] == nested_unpack(ast)

The only bit of magic is that `str_to_ast` will remove the Module that Python
assumes is the start of each string (as if it were its own file). With small
examples like this, we can fairly easily cover the AST concept by concept.

There's some more interesting stuff coming, but pytest makes it really easy to
do these little tests to build up confidence things are working as expected.

## Testing Win

Testing the BoolOp case quickly surfaced a
[typo](https://github.com/buckbaskin/random-python/commit/2dff8adf4104e5f2b086dcef874c583fa86e00ac#diff-9a7cc4f1e446f21dca1fcd2007a4cd6029f9460d38fb2bbd120c862da8fa018fL479-L486)

In the
[test](https://github.com/buckbaskin/random-python/commit/2dff8adf4104e5f2b086dcef874c583fa86e00ac#diff-6bb417164f20198c4e59062bb7b6b76426a82e595cb37ac5c1663f9df662c115R47-R49)
we have:

    def test_BoolOp():
        ast = str_to_ast("""name or False""")
        assert ["name"] == nested_unpack(ast)

But we get an error:

    E       AssertionError: assert ['name'] == [<ast.Name ob...7b7aa5140970>]
    E         At index 0 diff: 'name' != <ast.Name object at 0x7b7aa5140970>

The typo came down to returning the wrong thing: When iterating over the values
in a BoolOp, we kept returning the value instead of the name id...

    for v in element.values:
        for vid in nested_unpack(v, top_level):
            yield v

Becomes

    for v in element.values:
        for vid in nested_unpack(v, top_level):
            yield vid

Ultimately not a very complicated or insiduous bug, but definitely hard to
catch trying to drive-by inspect the code while reading a diff

# Logging

The other quick win for the day was logging. I'd originally been trying to
manage my own printing and debug info by passing around configuration, but
moving to using Python's built in logging library has made it much easier.

There's still some stuff that I'm trying to figure out (specifically indenting
the logging based on the depth of the iteration in the AST to make it easier to
visually see which data groups together) but for now I'm pretty satisfied with
being able to turn on debug information for an individual test but otherwise
keep the output pretty muted.
