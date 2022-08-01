---
Title: Starting the random-code journey
Category: Building
Tags: Open Source, random-python
Date: 2022-07-29
Updated: 2022-07-31
Summary: Let's automatically construct programs for testing
---

I got inspired by Zac Hatfield-Dodds's blog post 
[Sufficiently Advanced Testing](https://zhd.dev/sufficiently/). 
The post talks about [`hypothesis`](https://hypothesis.readthedocs.io/en/latest/)
and property based testing, but also goes into some other cool stuff:

- swarm testing
- coverage guided property-based testing ("Targeted PBT")
- symbolic execution
- concolic execution
- constructing programs

The last one is the one that stuck with me most. Quoting from the post:

> We could look at the grammar of Python source code, and we could generate arbitrary strings which would be parsed by the Python grammar. I tried this it worked! I found a bug in the CPython parser because it turns out that the grammar of Python is not exactly describing what CPython really does... foiled by the reference implementation!
>
> If this sounds cool, [you can use Hypothesmith too](https://pypi.org/project/hypothesmith/)! (punning on the more famous [CSmith](https://embed.cs.utah.edu/csmith/))
>
> The main challenge is that almost all syntactically-valid programs are semantically invalid, [which limits what we can test with them](https://blog.regehr.org/archives/1039). One promising approach is to [generate and 'unparse' a typed syntax tree](https://github.com/Zac-HD/hypothesmith/issues/2) - in particular, this could guarantee by construction that it's safe to execute the generated programs... so we could systematically compare Python interpreters as well as our development tools.

My interpretation of this was to jump into the challenge and see what I could do.

# An Inspiration: Wave Function Collapse

Wave function collapse has both a [physics
meaning](https://en.wikipedia.org/wiki/Wave_function_collapse) and also a exists
as name for an algorithm for procedural generation: [Maxim
Gumin's](https://github.com/mxgmn/Blog)
[WaveFunctionCollapse](https://github.com/mxgmn/WaveFunctionCollapse)

![Animated Gif demonstrating the states of wave function collapse for multiple source images](https://github.com/mxgmn/WaveFunctionCollapse/blob/a6f79f0f1a4220406220782b71d3fcc73a24a4c2/images/wfc.gif)

The procedural algorithm is inspired by the physics and attempts to
incrementally find the next piece to fit into the image based on samples from
the original source. From the README:

> WFC initializes output bitmap in a completely unobserved state, where each pixel value is in superposition of colors of the input bitmap (so if the input was black & white then the unobserved states are shown in different shades of grey). The coefficients in these superpositions are real numbers, not complex numbers, so it doesn't do the actual quantum mechanics, but it was inspired by QM. Then the program goes into the observation-propagation cycle:
>
> - On each observation step an NxN region is chosen among the unobserved which has the lowest Shannon entropy. This region's state then collapses into a definite state according to its coefficients and the distribution of NxN patterns in the input.
>  - On each propagation step new information gained from the collapse on the previous step propagates through the output.
>
> On each step the number of non-zero coefficients decreases and in the end we have a completely observed state, the wave function has collapsed.

# But Wait, You Said Something About Code, Not Images

We have the goal of generating random valid Python code and now an approach.
Following the basic steps from wave function collapse:

- On each step, pick a new ~region~ code block to "collapse" to a definite state
- Propagate new information to understand what code is valid

Right now at the start I don't have a good way to define entropy, so I'm taking
a simplified approach of taking a random ordering to fit code into. Based on
some [reading from Hyopthesmith's
README](https://github.com/Zac-HD/hypothesmith/blob/67fe54526964eac81cc2b355567e2bf565c38749/README.md)
random ordering will tend towards smaller example this will probably need to get
modified at some point to be more interesting.

For code, a "NxM" region doesn't make as much sense, so I've opted to use
[Python's Abstract Syntax Tree](https://docs.python.org/3.8/library/ast.html#abstract-grammar) (AST) to structure the process. The "region" of
interest is the AST node. At each step in visiting the tree, randomly select an
AST node of the same type to replace it. At the end, once we've visited every
node, we can reverse the parsing process and generate source code from the AST.

# So, what does that get us?

Based on the progress to the [latest
commit](https://github.com/buckbaskin/random-python/commit/7918c072822bfdd98fd02e364b3d8da8168cf0e8), a simple script that looks like:

    # python
    corpus_paths = list(find_files("corpus"))
    random_source = give_me_random_code(corpus_paths)

Produces output like:

    # python
    def factorial():
        if factorial == 1:
            return factorial - 1
        return 0
    if factorial <= 0:
        factorial(factorial - 1)

What's going on here? The script is searching the example corpus folder for
Python files. It finds some simple examples that have integer functions for
factorial, fibonacci and basic `main` function.

The `give_me_random_code` function then splits apart the AST by type (e.g.
FunctionDef) and replaces bits and pieces starting from the `Module` level.
Here we mostly see representation from the `factorial` function by name, but
some of the logic is based on fibonacci.

A satisfying element of working in Python in here is that it's quite quick to
get an example started and get something running. Now for the more complicated
bits for trying to ensure things are valid (executable)...

# References:

- [Zach Hatfield-Dodds](https://zhd.dev/)
- [hypothesis](https://github.com/HypothesisWorks/hypothesis/)
- [hypothesmith](https://github.com/Zac-HD/hypothesmith/)
- [Maxim Gumin](https://github.com/mxgmn) [@ExUtumno](https://twitter.com/ExUtumno)
- [Wave Function Collapse](https://github.com/mxgmn/WaveFunctionCollapse)
- [Python's Abstract Syntax Tree](https://docs.python.org/3.8/library/ast.html#abstract-grammar)

