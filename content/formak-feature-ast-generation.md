---
Title: AST Code Generation - New FormaK Feature
Category: Building
Tags: FormaK, Project FormaK, Code Generation, Python, C++
Date: 2023-06-12
Updated: 2023-10-30
Image: img/FstyleK.jpg
Summary: A new feature for FormaK has landed: improved model generation by leveraging a subset of the C++ Abstract Syntax Tree
---

FormaK aims to combine symbolic modeling for fast, efficient system modelling
with code generation to create performant code that is easy to use.

The new feature provides an extension to the fifth of the Five Keys "C++
interfaces to support a variety of model uses" by reworking how C++ generation
is done for easier extensions. After the 
[Calibration](blog/calibration-new-formak-feature.html) design, a lot of the code
templates looked like:

            StateAndVariance
            ExtendedKalmanFilter::process_model(
                double dt,
                const StateAndVariance& input
                // clang-format off
    {% if enable_calibration %}
                // clang-format on
                ,
                const Calibration& input_calibration
                // clang-format off
    {% endif %}  // clang-format on
                // clang-format off
    {% if enable_control %}
                // clang-format on
                ,
                const Control& input_control
                // clang-format off
    {% endif %}  // clang-format on
            ) {

Instead of relying on increasingly intricate Jinja templating and managing
formatting via flagging clang-format on and off, I instead opted for another
approach: generate the code from an abstract syntax tree (AST) that approximates
the Python and C++ AST. The reason to go with something that approximates the
Python AST is to have an inspiration and a guide from an AST that has
accumulated experience instead of reinventing the wheel (too much).

Afterwards, the code can look like:

    args = [
        Arg("double", "dt"),
        Arg("const StateAndVariance&", "input_state"),
    ]
    if enable_calibration:
        args.append(Arg("const Calibration&", "input_calibration"))
    if enable_control:
        args.append(Arg("const Control&", "input_control"))
    return FunctionDeclaration(
        "StateAndVariance",
        "process_model",
        args=args,
        modifier="",
    )

This approach isn't necessarily shorter, but it allows for replacing Jinja
templating with manipulating Python structures (primarily lists) in code. It
also generates cleaner code without droppings for clang-formatting.

Check out the [code](https://github.com/buckbaskin/formak/pull/13) or get the
latest updates for FormaK on [Github](https://github.com/buckbaskin/formak).

# What's next?

## Improving the AST Tooling

One stumbling block that I ran into while working on the code is consistency:
the AST has a structure that's repetitive (many functions with similar
arguments) but also every function has its own peculiarities, so I iterated
through multiple patterns for implementing this in a clear way. This indicates
to me an opportunity for improving the AST or providing a helper library that
uses the AST as a structure and helps streamline the code generation.

There is one code smell in the implementation of the AST generation that I opted
to leave in to meet my timeline for continuing onto the next feature: Escape.
The Escape AST member wraps a string and inserts the string during code
generation without any other structure. This was useful for quick hacks but
should probably get removed.

# 2023-06-29

Implementing the BasicBlock pattern during the
[Common Subexpression Elimination PR](https://github.com/buckbaskin/formak/pull/14)
allowed for cleaning up the last remaining uses of the Escape class in the AST
to inject a literal string. This was achieved by more tightly integrating the
BasicBlock code generation into the AST by yielding AST elements instead of
strings. In this way, I could instead "compile" the BasicBlock directly into the
AST instead of generating a string and passing it in as an Escape.
