---
Title: FormaK Week in Review 2023-01-13
Category: Building
Tags: Project Formak, FormaK, bazel, Week in Review, SIMD, Cpp, Python, Code Generation
Date: 2023-01-13
Updated: 2023-10-30
Summary: It's been a little while since I last wrote about Formak ( [FormaK Under The Hood: Optimization for scikit-learn integration](https://buckbaskin.com/blog/formak-u nder-the-hood-optimization-for-scikit-learn-integration.html) , Sat 08 October 2022). Since then, I've been busy adding functionality to FormaK and I've also been improving the tooling for the project, inspired by Boring Python: code quality. The latest piece of functionality is the C++ code generation. The PR is in progress, but the initial experiments have proved out that the generation pipeline is feasible and able to be integrated into bazel.
---

It's been a little while since I last wrote about Formak ( [FormaK Under The
Hood: Optimization for scikit-learn
integration](https://buckbaskin.com/blog/formak-u
nder-the-hood-optimization-for-scikit-learn-integration.html) , Sat 08 October
2022)

Since then, I've been busy adding functionality to FormaK:

- [Graph Editing / Graph Matching](https://github.com/buckbaskin/formak/pull/5) 
	- [SIMD and Graphs: Graph Matching](https://buckbaskin.com/blog/simd-and-graphs-graph-matching.html) 
- [Coffman Graham Ordering](https://github.com/buckbaskin/formak/pull/6) 
	- [SIMD and Graphs: Partitioning Graphs into data-dependency levels](https://buckbaskin.com/blog/simd-and-graphs-partitioning-graphs-into-data-dependency-levels.html) 
- [CPU Modeling](https://github.com/buckbaskin/formak/pull/7) 
	- [CPU Modeling: First Order Latency and Data Dependencies](https://buckbaskin.com/blog/cpu-modeling-first-order-latency-and-data-dependencies.html) 

I've also been [improving the
tooling](https://github.com/buckbaskin/formak/pull/8) for the project, inspired
by [Boring Python: code
quality](https://www.b-list.org/weblog/2022/dec/19/boring-python-code-quality/)

The latest piece of functionality is the [C++ code
generation](https://github.com/buckbaskin/formak/pull/9). The PR is in
progress, but the initial experiments have proved out that the generation
pipeline is feasible and able to be integrated into bazel.

# C++ Code Generation

Starting the week, the PR was in an experimental state. The code was
configured to generate C++ (really C) code from a sympy model. It's pretty
simple at this stage:

    :::python
    model = x * y + x + y + 1 
    ccode_model = ccode(model) 
    return {  
        "update_body": "_state += 1;", 
        "getValue_body": "return _state;", 
        "SympyModel_model_body": "return {};".format(ccode_model), 
    } 


## Complete the Two File Generation Experiment

The first step this week was to turn the prototype into something closer to the
final intended process by generating two files: the header file and the source
file. The initial experiment generated only one file and it turned out to
require some rethinking to get everything plugged together. Right now, this
looks like:
- Split out the template into a header and source template
- Update a bazel bash command with hand-rolled arguments and point the command at the various template files
- Update argparse in the Python code to read the hand-rolled arguments
- Update the code generation to take a simple path to determining the header include [this will come back to bite later]

This is a kinda long list to get right, so going forward I'd like to focus on simplifying it (or seeing if there can be a single source of truth). This focus might become second priority (and therefore not a priority) if it's something I can hide from the end user.

## Design Doc

The [design doc](https://github.com/buckbaskin/formak/blob/cpp-gen/docs/designs/cpp_library_for_model_evaluation.md) was heavily borrowed from the [Python design doc](https://github.com/buckbaskin/formak/blob/cpp-gen/docs/designs/python_library_for_model_evaluation.md) with updates to accommodate direct code generation vs a simpler sympy -> Python translation. I encourage you to read through it and send me feedback on your thoughts [@beBaskin](https://twitter.com/bebaskin).

## Making things official: Porting the experimental code to feature tests

Once I had a solid experiment and a design, I moved back to some of the code
logisitics, specifically setting up the feature tests for the design. There are
two feature tests:

1. UI -> C++: Simple 2D model of a parabolic trajectory converting from `ui.Model` to `cpp.Model`
2. Tooling: Simple 2D model of a parabolic trajectory converting from `ui.Model` to `cpp.ExtendedKalmanFilter`

For each test, what I hope to get out isn't too complicated: the Python -> code
gen -> C++ code should compile and pass a basic test or two. Getting there
wasn't quite so simple.

First, I recreated a lot of the Python pipework for C++. This means things like
test suites, tests and rearranging dependencies to distinguish between
languages (previously everything essentially behaved as a Python pip
dependency). To aid in an easy recreation of the experiment, I essentially
copied over the implementation of the experiment as a feature test and then
worked forwards (from the generation script) and backwards (from the C++ test)
to move to the feature test as designed.

While moving through half steps, the tricky to debug thing was a case of a
missing import of FormaK in the generation script. As of c5ee64 , this was the
limiting factor. The solution came down to replacing the `genrule` with a
`run_binary` Skylark rule instead. The underlying problem seems to be that the
genrule gets run in a basic environment instead of running with all bazel
dependencies populated. `run_binary` restricts what can be done, but when
configured with a dependency on the Python build target it gets the correct
environment. 3b8efa is the diff that fixed things if you want to dig further.

## Navigating C++ Code Generation

At this point, we have a C++ compile time error due to inadequacy in the code
generation. This is actually a good thing (:wave: hello from TDD land) because
it's fairly straightforward to fix knowing that we can iterate in the land of
C++. Before this point, problems could be Python problems (e.g. incorrectly
using the Jinja API), bazel problems (e.g. taking too many shortcuts when
creating a Skylark function) or C++ problems, but now they're just C++
problems. This means that we can proceed forward with essentially writing C++
to get a working solution, then extracting it out of the template into the code
generation logic and then cleaning things up to iterate towards the correct
solution.

## A `bazel` win!

Before I harp on this too much, I do want to celebrate a win: I'm happy with
how the [bazel/Skylark
rule](https://github.com/buckbaskin/formak/blob/cpp-gen/py/private/formak_gen.bzl#L5-L70)
for generating C++ from Python has turned out. Taking some liberties to clean
it up:

    :::python
    def cc_formak_model(name, pymain, pysrcs, pydeps = None, python_version = None, imports = None, visibility = None, **kwargs):
        PY_LIBRARY_NAME = name + "py-library-formak-model"
        PY_BINARY_NAME = name + "py-binary-formak-model"
        GENRULE_NAME = name + "genrule-formak-model"
        CC_LIBRARY_NAME = name
    
        ALWAYS_PY_DEPS = [
            "//py:formak",
            requirement("sympy"),
            requirement("Jinja2"),
        ]
    
        if pydeps == None:
            pydeps = []
    
        py_library(
            name = PY_LIBRARY_NAME,
            srcs = pysrcs,
            deps = pydeps + ALWAYS_PY_DEPS,
            imports = imports,
            visibility = ["//visibility:private"],
        )
    
        py_binary(
            name = PY_BINARY_NAME,
            srcs = [pymain],
            main = pymain,
            deps = [PY_LIBRARY_NAME],
            visibility = ["//visibility:private"],
        )
    
        MODEL_TEMPLATES = "//py:templates"
        OUTPUT_HEADER = "generated/formak/%s.h" % (name,)
        OUTPUT_SOURCE = "generated/formak/%s.cpp" % (name,)
        OUTPUT_FILES = [
            OUTPUT_HEADER,
            OUTPUT_SOURCE,
        ]
    
        run_binary(
            name = GENRULE_NAME,
            tool = PY_BINARY_NAME,
            args = ["--templates", "$(locations " + MODEL_TEMPLATES + ")", "--header", "$(location generated/formak/%s.h)" % (name,), "--source", "$(location generated/formak/%s.cpp)" % (name,)],
            outs = OUTPUT_FILES,
            srcs = ["//py:templates"],
        )
    
        native.cc_library(
            name = CC_LIBRARY_NAME,
            srcs = [OUTPUT_SOURCE],
            hdrs = [OUTPUT_HEADER],
            strip_include_prefix = "generated",
            deps = [],
            visibility = visibility,
        )

Breaking it down, we can see that it's not doing too much magic. The Python
file(s) are collected into a library, then used to run the binary dependency
(this seems like it might be an extra step, but I'll stick with it for now).
The Python binary is then used to run the `run_binary` step which generates C++
code files. The code files are then compiled as sources of the final C++
library. Using bazel visibility rules, we can restrict things to essentially
just the output C++ library being visible, so the rule (from the outside) looks
like we give it Python source files and get back a C++ library interface. All
without having to do anything custom-looking in Bazel land.

# A taste of what’s coming next

- Completing C++ generation of models
- C++ generation of an EKF to quantify error behavior

