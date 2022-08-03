---
Title: random-code Day 2
Category: Building
Tags: Open Source, random-python, Project Random
Date: 2022-07-30
Updated: 2022-07-31
Summary: Progress on a better understanding of Python while generating random code
---

I got inspired by Zac Hatfield-Dodds's blog post [Sufficiently Advanced
Testing](https://zhd.dev/sufficiently/) to pursue the challenge of construction
random programs. To get the intro of what I've worked on so far check out the
[Day 1 post](blog/starting-the-random-code-journey.html)

# Progress

When I left off yesterday, I had a simple code and corpus example working, but I need to take further steps to get it working on real code.

## Name Discovery

In order to figure out which names are in scope and which names we need to
match, we need to inspect the underlying tree. For example, if the new code
swapped in references `self.clear()`, we want do break it down and identify
that we want to check the scope for `self`.

- Later we can do some type checking that will help us known if self has a
  callable member `clear`

For this example, `self.clear()` starts out as the AST node `Call`. Under it,
we have an `Attribute` `.func`. This has the two elements of interest:

- attr `clear`
- value, which is a `Name` with id `self`

In order to solve this, we can recursively search an AST for names that we need
to check in scope. This is done by the
[`nested_unpack`](https://github.com/buckbaskin/random-python/blob/8802d4fb5dafd71eb0637ef2531e81079449d9ad/random_code/impl.py#L397-L665)
method. (It's not the cleanest, but...) The general pattern is for each type to
either identify if:

- There's no possible names we'd need to check (e.g. for a `Constant`)
- There's one possible name (e.g. for a `Name` where we want it's `id`)
- There's multiple possible subelements that could have names

To combine these together, each function retuns the list, and elements that
contain multiple sub-elements flatten the list from their sub-elements and call
the recursion. This rolls up to a list at the top level of 0 or more names to
check and pretty elegantly fits into the scope checking code.

## Scoping

Each each element, we know if we've defined more names (e.g. for an `Assign`)
or gotten into a new scope (e.g. for a FunctionDef) and new names (e.g.
arguments in a `FunctionDef`).

This isn't something I've found a good general pattern for and haven't yet
gotten to all the sources of names and scopes, so the code is sticking to hard
code in the visiting logic
[`_visit_X`](https://github.com/buckbaskin/random-python/blob/8802d4fb5dafd71eb0637ef2531e81079449d9ad/random_code/impl.py#L853-L861)
for function arguments.

## Validating Swaps in the AST

Together, we can use the name discovery and scoping to aid in doing a better
job than randomly swapping by AST type. For each potential swap we're checking,
we can make sure that the names we're swapping in are going to be in scope when
they're used. This shakes out as the basic end conditions for
[`valid_swap`](https://github.com/buckbaskin/random-python/blob/8802d4fb5dafd71eb0637ef2531e81079449d9ad/random_code/impl.py#L808-L813).

This swap validation feels like it could be done more recursively like the name
discovery, but I haven't figured out that pattern yet.

### Special Case: Typing

When it comes to swapping out names, I've implemented a primative type matching
system. When I find cases where I know the type (e.g. from Python type
annotations), I store the variable's type as the value in the key-value mapping
in the scope (with the name as the key). This allows for swapping exact type
matches, but there's no sense of classes and sub-classes without doing a little
bit more.

(I think the little bit more would be tracking class definitions and parent
classes in an auxiliary tree)

### Special Case: Function Calls

This feels like it might not need to be a special case, but for now it is to
handle making sure that the position and keyword arguments that go into the
function call are all checked. This special case does have some weird edge case
behavior. For example, calling `"a b c".split(" ")` doesn't have a name to
validate even though my intuition is that usually we'd expect to have at least
one name to validate.

# References:

- [Zach Hatfield-Dodds](https://zhd.dev/)
- [Sufficiently Advanced Testing](https://zhd.dev/sufficiently/)

