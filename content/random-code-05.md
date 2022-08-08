---
Title: random-code Day 5: Python Class Manipulation
Category: Building
Tags: Open Source, random-python, Project Random
Date: 2022-08-03
Updated: 2022-08-07
Summary: Becoming a little more familiar with Python's Abstract Base Class functionality
---

I got inspired by Zac Hatfield-Dodds's blog post [Sufficiently Advanced
Testing](https://zhd.dev/sufficiently/) to pursue the challenge of construction
random programs. To get the intro of what I've worked on so far check out the
[Day 1 post](blog/starting-the-random-code-journey.html) and the latest [Day 4
post](blog/random-code-day-4-littering.html). Check out the
[random-python](https://github.com/buckbaskin/random-python) project on
Github.

# Type Dispatching

In the AST visiting logic, there are a handful of functions that all need to
dispatch to different logic based on the type of the node they're working with.
They all look something like:

    def interesting_node_logic(node):
        if isinstance(node, FunctionDef):
            ...
        elif isinstance(node, Lambda):
            ...
        elif isinstance(node, ListComp):
            ...
        ...

This continues on for quite a while because there are 40 or 50 different types
of nodes we can encounter in the tree. Even if each only needs a couple of
lines of logic, this can lead to long piles of code. If we can find more
succinct ways to represent these functions, we can more easily group similar
logic and compress the code into more readable groups of lines instead of
having sprawling logic and repeated code.

# Abstract Base Classes

I recently ran across [Hillel Wayne's](twitter.com/hillelogram) blog post
["Crimes with Python's Pattern
Matching"](https://www.hillelwayne.com/post/python-abc/) about pattern matching
and Python's abstract base classes. It starts off with a bang:

> One of my favorite little bits of python is `__subclasshook__`. Abstract Base Classes with `__subclasshook__` can define what counts as a subclass of the ABC, even if the target doesn’t know about the ABC.

This first few sentences of the blog post provided me with all I needed to know
to figure out how to simplify the type dispatching. For AST elements with
similar properties, we can create groups to make them easier to work with. 

The immediate example that comes to mind is called
[`NotNameParent`](https://github.com/buckbaskin/random-python/blob/1d9d170b6b907759be2a9b2b900c62e0939ec147/random_code/impl.py#L145-L160).
When parsing an AST looking for names that need to be in scope, there are a
handful of AST nodes that we know will not contain a name to check and will not
have children with a name to check. These include: `break`, `pass` and
constants. This means that we can create a simple abstract base class that
collects these names into a single consistent idea. The class looks like:

    class NotNameParent(ABC):
        _doesnt_contain_names = {
            "Break",
            "Constant",
            "Import",
            "ImportFrom",
            "JoinedStr",
            "NoneType",
            "Pass",
        }
    
        @classmethod
        def __subclasshook__(cls, C):
            name = C.__name__
            log.debug("NotNameParent.__subclasshook__ %s", name)
            return name in cls._doesnt_contain_names

And allows us to simplify the type dispatching logic to [lines
like](https://github.com/buckbaskin/random-python/blob/1d9d170b6b907759be2a9b2b900c62e0939ec147/random_code/impl.py#L496-L497):

    if isinstance(element, NotNameParent):
        return []

# Conclusion

In conclusion, there's Python mechanisms under the hood that can greatly
simplify repetitive code if only you know where to look. Abstract Base Classes
let you retroactively combine different classes across similar concepts to
create an alternate tree for your use case.

Also, I highly recommend reading more than just the first paragraph of Hillel's
post ["Crimes with Python's Pattern
Matching"](https://www.hillelwayne.com/post/python-abc/). It's well written and
fascinating.
