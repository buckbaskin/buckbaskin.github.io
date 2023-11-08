---
Title: The Simplify Speedup Experiment
Category: Building
Tags: FormaK, Project FormaK, Python, Sympy, Profiling
Date: 2023-11-07
Updated: 2023-11-07
Image: img/pstats_simplify.svg
Summary: Over multiple iterations of improving FormaK (reference IMU model rocket model, the original Python code generation), I've wanted to leverage the power of Sympy to provide efficient implementations of symbolic concepts before converting to Python or C++. The tool for this job is `simplify`. With one call, it can simplify polynomials, simplify trigonometry and other approaches. Combine this with Common Subexpression Elimination and we have a powerful pair of tools to write efficient code regardless of the model. There's just one problem: Sympy can be incredibly sluggish for some functions. Each call can take 10s of seconds. These 10s of seconds can stack up to minutes of time spent waiting and hoping for a result. For this experiment, I take some time to dive into what's going on and try to understand why it can be so darn slow sometimes.
---

Over multiple iterations of improving FormaK ([reference IMU
model](/blog/strapdown-imu-reference-model-new-formak-feature.html), [rocket
model](/blog/calibration-new-formak-feature.html), the [original Python code
generation](/blog/formak-python-code-generation.html)), I've wanted to leverage
the power of Sympy to provide efficient implementations of symbolic concepts
before converting to Python or C++.

The tool for this job is
[`simplify`](https://docs.sympy.org/latest/tutorials/intro-tutorial/simplification.html#simplify)
([API
docs](https://docs.sympy.org/latest/modules/simplify/simplify.html#sympy.simplify.simplify.simplify)).
With one call, it can simplify polynomials, simplify trigonometry and other
approaches. Combine this with [Common Subexpression
Elimination](https://docs.sympy.org/latest/modules/rewriting.html#common-subexpression-detection-and-collection)
and we have a powerful pair of tools to write efficient code regardless of the
model.

There's just one problem: Sympy can be incredibly sluggish for some
expressions. Each call can take 10s of seconds. These 10s of seconds can stack
up to minutes of time spent waiting and hoping for a result. For this
experiment, I wanted to take some time to dive into what's going on and try to
understand why `simplify` can be so darn slow sometimes.

# Experiment Setup

The first part of the experiment was to make a slow expression. Taking
inspiration from a particularly slow case in the reference IMU design, I opted
to simplify expressions for converting from rotation matrices to quaternions
then back to rotation matrices.

    slow_expr = Quaternion.from_rotation_matrix(reference).to_rotation_matrix()

This results in long polynomials that (apparently) result in a large
simplification burden. To find a slow-but-not-too-slow expression, I performed
a bottoms up traversal of the slow expression until I got an expression taking
~10 seconds to simplify.

    (a/4 + e/4 + i/4 - (-a - e + i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h -
    c*e*g)**(1/3))*sign(-b + d)**2/4 - (-a + e - i + (a*e*i - a*f*h - b*d*i + b*f*g
    + c*d*h - c*e*g)**(1/3))*sign(c - g)**2/4 + (a - e - i + (a*e*i - a*f*h - b*d*i
    + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-f + h)**2/4 + (a*e*i - a*f*h - b*d*i +
    b*f*g + c*d*h - c*e*g)**(1/3)/4)/(a/4 + e/4 + i/4 + (-a - e + i + (a*e*i -
    a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-b + d)**2/4 + (-a + e - i
    + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(c - g)**2/4 + (a
    - e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-f +
    h)**2/4 + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3)/4)

# Profiling

The profiling is built on Python's
[cProfile](https://docs.python.org/3/library/profile.html). It's not exactly
performant, but it's easy enough to take a function invocation:

    simplify(expr)

and convert the function call to a profiling exercise that can yield
information about the function's inner timings:

    cProfile.runctx(
        "simplify(expr, inverse=False)",
        globals=globals(),
        locals={"expr": expr},
        filename=filename
    )

This profiling provides lots of information, such as the cumulative time in a
function or the time spent in the function specifically (excluding
sub-functions). Unfortunately, that lots of information is often too much
information to understand intuitively during an exploratory exercise such as
this one where I'm not familiar with the code.

## Flamegraphs

Flamegraphs to the rescue! Flamegraphs show function timing via samples (on the
horizontal axis) and then the call dependencies on the vertical axis. I love
the way they look and they're also flexible for quickly understanding function
performance. If a function has a material number of calls, then it will stand
out visually, but if there is a mix of calls (or none of the calls you expect)
then it's worth investing in further exploration to better understand the
problem because there's not a clear performance win to be had at that stage.

![Flamegraph showing various long running functions]({attach}/img/pstats_simplify.svg)

The flamegraph for this shows time going to `cancel`, which itself is split
between `factor_terms` and `sign_simp`. `factor_terms` is built of a recursive
series of calls to `gcd_terms` (which makes sense) but does obscure the timing
of related functions and where there may be a performance improvement.

# Results?

In the time I had for this experiment, I wasn't able to get anything to a
particularly satisfying conclusion. I have a few more hypothesis to check
(perhaps common subexpression elimination could be used to speed up the
simplify process?) but for now I remain stuck. Simplification may remain a
final finishing step for a "release" build and won't be actively used quite yet
in the FormaK design and development process.

# Bonus Round

I got a suggestion from [@hugovk](https://mastodon.social/@hugovk) to try out the latest Python release:

[https://fosstodon.org/@hugovk@mastodon.social/111351314621822006](https://fosstodon.org/@hugovk@mastodon.social/111351314621822006)

> If you're not already, you could compare Python 3.12:
> 
> "Dictionary, list, and set comprehensions are now inlined, rather than creating a new single-use function object for each execution of the comprehension. This speeds up execution of a comprehension by up to two times." 
> 
> [https://docs.python.org/3/whatsnew/3.12.html#whatsnew312-pep709](https://docs.python.org/3/whatsnew/3.12.html#whatsnew312-pep709)
> \#Python \#Python312 \#PEP709

The overall trend that I found was the performance on 3.10 and 3.11 were close,
but 3.12 performance was actually slower than the other two. It seems like lots
of libraries are making major updates for 3.12 (as well as the fact that list
comprehensions are getting a speedup), so it may be the case that as libraries
update the performance will return to parity or surpass the performance of the
libraries executing on 3.10.

I've included the data from profiling below. 

## 3.12 version e991b8c

    Python Version sys.version_info(major=3, minor=12, micro=0, releaselevel='final', serial=0)
    Slow Expression
    (a/4 + e/4 + i/4 - (-a - e + i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-b + d)**2/4 - (-a + e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(c - g)**2/4 + (a - e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-f + h)**2/4 + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3)/4)/(a/4 + e/4 + i/4 + (-a - e + i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-b + d)**2/4 + (-a + e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(c - g)**2/4 + (a - e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-f + h)**2/4 + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3)/4)
    Begin Profiling
    End Profiling
    Profiling took about 58.970478 seconds
    Tue Nov  7 00:50:37 2023    simplify_pstats
    
             83403827 function calls (71409971 primitive calls) in 58.891 seconds
    
       Ordered by: cumulative time
       List reduced from 1377 to 10 due to restriction <10>
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        512/1    0.066    0.000   58.902   58.902 {built-in method builtins.exec}
        147/1    0.007    0.000   58.902   58.902 simplify.py:420(simplify)
            1    0.000    0.000   55.085   55.085 piecewise.py:1333(piecewise_simplify)
            1    0.000    0.000   54.667   54.667 piecewise.py:1145(piecewise_simplify_arguments)
          203    0.006    0.000   44.180    0.218 polytools.py:6801(cancel)
           68    0.001    0.000   41.195    0.606 expr.py:3788(cancel)
          389    0.001    0.000   35.406    0.091 exprtools.py:1156(factor_terms)
    148423/389    0.681    0.000   35.404    0.091 exprtools.py:1217(do)
         9880    0.109    0.000   32.502    0.003 exprtools.py:980(gcd_terms)
         9880    0.262    0.000   32.006    0.003 exprtools.py:915(_gcd_terms)

Reruns:

- 83462111 function calls (71463102 primitive calls) in 59.368 seconds
- 83402767 function calls (71409367 primitive calls) in 60.314 seconds

## 3.11 Version 486a2eb

    Python Version sys.version_info(major=3, minor=11, micro=6, releaselevel='final', serial=0)
    Slow Expression
    (a/4 + e/4 + i/4 - (-a - e + i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-b + d)**2/4 - (-a + e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(c - g)**2/4 + (a - e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-f + h)**2/4 + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3)/4)/(a/4 + e/4 + i/4 + (-a - e + i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-b + d)**2/4 + (-a + e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(c - g)**2/4 + (a - e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-f + h)**2/4 + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3)/4)
    Begin Profiling
    End Profiling
    Profiling took about 51.619768 seconds
    Tue Nov  7 00:52:18 2023    simplify_pstats
    
             84451839 function calls (72211354 primitive calls) in 51.589 seconds
    
       Ordered by: cumulative time
       List reduced from 1564 to 10 due to restriction <10>
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        513/1    0.047    0.000   51.599   51.599 {built-in method builtins.exec}
        147/1    0.007    0.000   51.599   51.599 simplify.py:420(simplify)
            1    0.000    0.000   48.176   48.176 piecewise.py:1333(piecewise_simplify)
            1    0.000    0.000   47.823   47.823 piecewise.py:1145(piecewise_simplify_arguments)
          203    0.007    0.000   38.900    0.192 polytools.py:6801(cancel)
           68    0.001    0.000   36.493    0.537 expr.py:3788(cancel)
          389    0.001    0.000   31.691    0.081 exprtools.py:1156(factor_terms)
    148423/389    0.839    0.000   31.689    0.081 exprtools.py:1217(do)
     9088/405    0.024    0.000   29.952    0.074 exprtools.py:1242(<listcomp>)
    21008/538    0.043    0.000   29.707    0.055 exprtools.py:1263(<listcomp>)

Reruns

- 84435622 function calls (72194285 primitive calls) in 53.926 seconds
- 84430371 function calls (72188205 primitive calls) in 51.855 seconds

## 3.10 Version 21aaae8

    Python Version sys.version_info(major=3, minor=10, micro=13, releaselevel='final', serial=0)
    Slow Expression
    (a/4 + e/4 + i/4 - (-a - e + i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-b + d)**2/4 - (-a + e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(c - g)**2/4 + (a - e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-f + h)**2/4 + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3)/4)/(a/4 + e/4 + i/4 + (-a - e + i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-b + d)**2/4 + (-a + e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(c - g)**2/4 + (a - e - i + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3))*sign(-f + h)**2/4 + (a*e*i - a*f*h - b*d*i + b*f*g + c*d*h - c*e*g)**(1/3)/4)
    Begin Profiling
    End Profiling
    Profiling took about 50.896008 seconds
    Tue Nov  7 00:54:13 2023    simplify_pstats
    
             84462355 function calls (72217560 primitive calls) in 50.865 seconds
    
       Ordered by: cumulative time
       List reduced from 1552 to 10 due to restriction <10>
    
       ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        513/1    0.058    0.000   50.878   50.878 {built-in method builtins.exec}
            1    0.000    0.000   50.877   50.877 <string>:1(<module>)
        147/1    0.007    0.000   50.877   50.877 simplify.py:420(simplify)
            1    0.000    0.000   47.561   47.561 piecewise.py:1333(piecewise_simplify)
            1    0.000    0.000   47.213   47.213 piecewise.py:1145(piecewise_simplify_arguments)
          203    0.006    0.000   38.083    0.188 polytools.py:6801(cancel)
           68    0.001    0.000   35.561    0.523 expr.py:3788(cancel)
          389    0.001    0.000   30.927    0.080 exprtools.py:1156(factor_terms)
    148423/389    0.838    0.000   30.925    0.079 exprtools.py:1217(do)
     9088/405    0.023    0.000   29.286    0.072 exprtools.py:1242(<listcomp>)

Reruns:

- 84422661 function calls (72181588 primitive calls) in 50.693 seconds
- 84433281 function calls (72191175 primitive calls) in 49.238 seconds

