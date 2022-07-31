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

# An Aside: Wave Function Collapse

Wave function collapse has both a [physics meaning](https://en.wikipedia.org/wiki/Wave_function_collapse)
and also a exists as name for an algorithm for procedural generation: 
[mxgmn's WaveFunctionCollapse]https://github.com/mxgmn/WaveFunctionCollapse

https://github.com/mxgmn/WaveFunctionCollapse/raw/master/images/wfc.gif


