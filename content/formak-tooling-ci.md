---
Title: FormaK Tooling: CI
Category: Building
Tags: FormaK, Project FormaK,30 for 30, GitHub, GitHub Actions
Date: 2022-10-07
Updated: 2022-10-04
Summary: FormaK implements CI for new commits as of PR #4 via GitHub Actions
Image: img/github-actions-example.jpg
---

TLDR: FormaK implements CI for new commits as of [PR #4](https://github.com/buckbaskin/formak/pull/4) via GitHub
Actions

This post aims to be a short review of FormaK’s tooling for continuous
integration (CI). 

In the [design of the
library](https://github.com/buckbaskin/formak/blob/master/docs/designs/formak_v0.md),
FormaK aims to deal with a handful of big features:

- Code generation across languages
- Detailed numerical code (the [`scikit-learn` integration](https://github.com/buckbaskin/formak/blob/sklearn-integration/docs/designs/sklearn-integration.md) for example)

FormaK’s design process also leans on testing as part of the design phase
(feature tests) and refactoring with confidence in addition to tests for
correctness and numerical properties (property-based testing). Altogether,
automatic testing is incredibly useful to the project.

The original format for this testing was a bash file: 
[`actions/ci.bash`](https://github.com/buckbaskin/formak/blob/17199f85d98623395eba3556fcb24214e958f3f6/actions/ci.bash).
This runs the tests for the project in multiple configurations, but requires
remembering to run locally. As a convinience, the project also has a Makefile
to enable the command `make ci` but that doesn’t solve the missing automation.

Instead, the FormaK project now uses GitHub Actions to run these tests
automatically. The configurations can be seen in
[.github/workflows](https://github.com/buckbaskin/formak/tree/17199f85d98623395eba3556fcb24214e958f3f6/.github/workflows),
with one each for:

- Feature tests: do they pass?
- Demos: do they run?
- Unit tests: do they pass?

This integrates automatically with Github PRs to give the following:

![Example of Github Actions with one test failing]({attach}/img/github-actions-example.jpg)

All in all, this seems to work pretty well. I read ["How well do you know
Github
Actions?"](https://fusectore.dev/2022/09/25/github-actions-pitfalls.html) and
expected to have it fall apart, but following GitHub's
[Quickstart](https://docs.github.com/en/actions/quickstart) got me 95% of the
way there.

