---
Title: Design Driven Design
Category: Building
Tags: FormaK, Project FormaK, Design, Python, C++, hypothesis
Date: 2024-04-03
Updated: 2024-04-03
Image: img/FstyleK.jpg
Summary: Design Driven Design builds feedback loops that allow for continuous improvements to open source projects during each pull request. The loops are: Design Writing informs Feature Testing which in turn informs the Design, Feature Testing informs Unit Testing which in turn informs the Feature Testing, Unit Testing informs Design Writing which in turn informs the Unit Testing. These loops form seams for collaboration across partners or for self-re-evaluation at mindful points in the process to maximize success.
---

Design Driven Design builds feedback loops that allow for continuous
improvements to open source projects during each pull request.
The loops are:
- Design Writing informs Feature Testing which in turn informs the Design
- Feature Testing informs Unit Testing which in turn informs the Feature Testing
- Unit Testing informs Design Writing which in turn informs the Unit Testing

These loops form seams for collaboration across partners or for
self-re-evaluation at mindful points in the process to maximize success.

# Outline

The Design Driven Design process follows three stages:
1. Write a design document about the feature, its benefits and key details for
   the solution approach
2. Write a feature test (or tests) that capture the essential behavior of the
   feature
3. Implement a prototype version that makes the 
3. Write unit tests that more completely specify the detailed behavior of the
   feature

But wait, where are the loops? This looks kind of like waterfall!

# The Design and Feature Testing Loop

The first loop is between writing the design and implementing a feature test.

When writing the design, it's helpful to think about how you'd know if a feature
was working. This test for if the feature seems to be working is the first
feature test.

Writing the feature test will expose vagueness in writing or missing portions of
the design when it fails to convert nicely to code. The feature test will also
expose if an interface is hard to use correctly, which can inform updates to the
design.

Together, the design can be improved and the initial testing can be improved by
working on the two in an alternating loop. This improved end state after
looping makes it easier to proceed with an implementation knowing the interface
is more likely to be settled in a good state and the implementation can have
initial feedback on a pass-fail basis (or even better, multiple assertion
conditions) based on the feature test.

Unit testing can expand on this loop to surface additional poorly specified
aspects of the design, missing features from the solution approach and other
aspects. It should also be used to inform feedback in the design.

# The Feature Testing and Unit Testing Loop

Often times a feature test can provide a high level view that informs initial
development, but it takes unit testing to make the implement concrete and fully
thought out. For example, it is often burdensome to capture all possible edge
cases in an end to end feature test (and attempting this also reduces the value
of the feature test as a demonstration of how to use the feature). Unit tests
can step in to fill this gap by defining the expected behavior in code.

Unit testing the feature can also provide feedback in cases where the design is
hard to test. This helps improve the implementation and the feature test by
encouraging splitting the implementation into smaller and/or more testable
parts. This can often lead to splitting the feature test into multiple parts that
make for more illustrative examples. This can also lead to opportunities to
simplify the feature test by offloading some behavioral checks to unit tests

# Bonus: Cross-Language Improvement Loops

The [FormaK](https://buckbaskin.com/blog/tag/project-formak.html) library
([Github](https://github.com/buckbaskin/formak)) adds an additional feedback
loop by cross-pollinating improvements between C++ and Python. While writing
Python functionality, the algorithms or data structures can often be improved by
thinking through how I'd have to implement the same algorithm in C++ or by
adding types to make interfaces self-documenting. The C++ benefits from a first
pass of an algorithm in Python where an algorithm can often be written closer to
pseudo-code and complications and failed implementation approaches in Python can
inform areas where specific C++ patterns could be helpful (e.g. where to
introduce strong types so two quantities aren't mixed).

One concrete example of this feedback loop is property-based testing, which
originated as a Python testing feature with the
[`hypothesis`](https://hypothesis.readthedocs.io/en/latest/) library and then
expanded to a C++ testing feature
[`rapidcheck`](https://github.com/emil-e/rapidcheck).

# The Bonus Nobody Wanted

Wikipedia actually indicates that 
["Royce's final model"](https://en.wikipedia.org/wiki/Waterfall_model)
of waterfall actually incorporated these feedback loops.
