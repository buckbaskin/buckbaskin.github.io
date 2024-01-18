---
Title: FormaK Tooling: Documentation
Category: Building
Tags: FormaK, Project FormaK, GitHub, GitHub Actions, Documentation, Open Source
Date: 2024-01-17
Updated: 2024-01-17
Summary: FormaK implements a new documentation builder to make documentation much easier to navigate and look better too.
Image: img/FormaKDocsBoth.jpg
---

TLDR: FormaK moved to Sphinx documentation and documentation checks in CI for
new commits as of
[c8ae13e](https://github.com/buckbaskin/formak/commit/c8ae13e9810a9915f8a8721c40e185b04d47ceee)

This post aims to be a short review of FormaK’s tooling for documentation.

# Motivation

The goal for this effort was to improve the organization and the look and feel
of the FormaK documentation. Many Python projects have nice looking
documentation and FormaK documentation felt out of place. In addition, ease of
use is a key value for the FormaK project and the documentation was decidedly
not easy to use.

![Documentation before the changes with a black and white style and no navigation]({attach}/img/FormaKDocsBefore.jpg)

As an additional motivating factor, the helpful resource [Producing Open
Source Software](https://producingoss.com/) heavily emphasizes the importance
of
[documentation](https://producingoss.com/en/getting-started.html#documentation).
As part of getting off to a good start for the year, I've been re-reviewing the
suggestions there and trying to more enthusiastically adopt them to fit the
FormaK project.

# Solution Approach

My initial familiarity for documentation tooling was largely based on the blog
(built on Pelican) which quite blog focused and requires significant effort for
applying a theme.

I had the following criteria for the tooling:
- it shouldn't be blog focused
- it should have easy support for existing Markdown documentation
- it should be easy to apply a good-enough looking theme

## Research

I started my research with the [scikit-learn
documentation](https://scikit-learn.org/). It's quite good looking, it has
useful organizational and navigational information and it's style seems
representative of Python documentation that I like. Poking around the site
turns up the documentation for [contributing
documentation](https://scikit-learn.org/dev/developers/contributing.html#documentation)
and specifically [building the
documentation](https://scikit-learn.org/dev/developers/contributing.html#building-the-documentation).
In that we can see that the tool
[Sphinx](https://www.sphinx-doc.org/en/master/) is the first pip dependency.

Taking a look through Sphinx, it was pretty clearly documentation focused and
has a focus on aesthetics. The remaining hurdle was understanding if it could
inter-operate with minimal changes to existing documentation.

Out of the gate, Sphinx is designed to work with reStructuredText markup
language, but also supports a flavor of Markdown called [MyST
markdown](https://www.sphinx-doc.org/en/master/usage/markdown.html#markdown).
Boom, we have our tool.

## Steps along the way

Identifying sphinx and setting up a pip dependency didn't immediately lead to
nice documentation. Sphinx has nice [Getting
Started](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
documentation, but then I immediately had to divert to the [Markdown
documentation](https://www.sphinx-doc.org/en/master/usage/markdown.html#markdown).
In switching to Markdown early, I missed the concept of the `toctree` and had
to re-discover this later in the process. Save yourself the trouble and read
the full Getting Started page first before jumping around.

The documentation I'd written so far makes use of LaTeX for mathematical
notation. This was initially broken in the first few rounds of documentation
generation, but now it's supported via MyST [Syntax
Extensions](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html).
`amsmath` and `dollarmath` where the two keys for LaTeX support, but I opted to
enable a number of additional extensions:
- "fieldlist" (leading metadata for design docs)
- "linkify" (better link handling)
- "strikethrough"
- "tasklist" (add support for [ ], [x] tasks)

The final piece of the puzzle is `autodoc`. This is the Sphinx integrated
tooling for automatically generating API documentation from Python files. This
is something that's only partially useful (due to my lack of docstrings, yes,
I'm working on it), but will improve as the project ages and more of the
modules, functions and classes get docstrings as they're updated.

On the theme front, I ended up swapping to the "classic" theme to get something
that looked even more Pythonic than the default theme too. 

Keeping docs up to date has a few approaches. There are ways to integrate
third-party tools (like Read The Docs) or to use Github Actions to generate new
docs on the fly; however, I opted for a simpler approach. As of PR
[#23](https://github.com/buckbaskin/formak/pull/23), the documentation is
checked into the source tree and then a Github Action merely checks to see if
there's a diff when re-generating the documentation. This has the benefit of
having the documentation available immediately for anyone downloading the
project and removes any complexity of managing git branches via Github Actions
or trying to add commits via Github Actions to generate the documentation.

There were also some hidden benefits to Sphinx. For one, it does some amount of
validation of the documentation structure for pages that aren't accessible as
part of a table of contents. It also does validation of the documentation
structure to ensure it makes sense (e.g. not skipping header levels).

P.S. Sphinx plays much better with Github Pages if you include the `.nojekyll`
file in the top level of the docuemnts directory. If not, static files will be
skipped by Github Pages and it'll break the javascript and CSS for the site.

# The Result

Before

![Documentation before the changes with a black and white style and no navigation]({attach}/img/FormaKDocsBefore.jpg)

After

![Documentation after the changes with a blue style and a table of contents]({attach}/img/FormaKDocsAfter.jpg)

One of the key things to note is the navigation aids (table of contents on the
left, breadcrumbs for file organization along the top). Overall it is much
better and the improvements will continue to compound as the project grows its
API documentation and user documentation.
