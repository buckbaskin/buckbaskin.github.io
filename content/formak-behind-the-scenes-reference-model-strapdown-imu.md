---
Title: Behind the Scenes of the Strapdown IMU Reference Model
Category: Building
Tags: FormaK, Project FormaK, Python, C++, IMU, Strapdown IMU, Sympy
Date: 2023-10-30
Updated: 2023-10-30
Image: img/FstyleK.jpg
Summary: A new feature for FormaK has landed: the Strapdown IMU Reference model. The model is now available for inclusion into new models and use as a reference for implementing future models. This post covers some of the aspects of the design and development that didn't make it into the final design and feature.
---

A new feature for FormaK has landed: the Strapdown IMU Reference model. The
model is now available for inclusion into new models and use as a reference for
implementing future models. This post covers some of the aspects of the design
and development that didn't make it into the final design and feature.

If you're interested in the reference model, you can read the
[launch announcement](/blog/strapdown-imu-reference-model-new-formak-feature.html).

Pull Request: [#19](https://github.com/buckbaskin/formak/pull/19)

Commit: [16ba541](https://github.com/buckbaskin/formak/tree/16ba541e799dfe1b289618a7b27ec48847191172)

# The Rotation Class

A few days into the project I decided it'd be a good idea to develop a general
purpose Rotation class that could serve as a simple conceptual object that
could also be easily be compiled into different representations for any model.

This was mostly an exercise in learning that I should do a bit of searching
around before I make such an attempt. I spent three weeks making this class,
testing it to a 80% level of completion, then refactoring to pull it out and
replace it with the
[Sympy Quaternion](https://docs.sympy.org/latest/modules/algebras.html) class
that offered the same feature set but in working order and with tests.

N.B. Scipy also has a 
[Rotation class](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html)

# Pytest Features

Pytest has functionality for
[skipping failing tests](https://docs.pytest.org/en/6.2.x/skipping.html). It
also supports marking tests as
[`xfail`](https://docs.pytest.org/en/6.2.x/skipping.html#xfail-mark-test-functions-as-expected-to-fail),
which will run the test and then fail the test run if the test passes.

    @pytest.mark.xfail
    def test_function():
        ...

Pytest also supports
[parameterized tests](https://docs.pytest.org/en/7.1.x/example/parametrize.html)
. While I was implementing a generic Rotation class with multiple underlying
representations (Euler angles, rotation matrices and quaternions), I could use
the feature to easily run the same test across all representations to make sure
it passed. It leads to nicely formatted test outputs (until you multiply your
failures then there's just too much text scrolling by).

Abridged Code:

    REPRESENTATIONS = ["quaternion", "matrix", "euler"]
    
    @pytest.mark.parametrize("representation", REPRESENTATIONS)
    def test_principal_axis(representation):
        ...

Sample Output:

    =========================== short test summary info ============================
    FAILED py/test/unit/rotation_test.py::test_principal_axis[matrix] - assert False
    FAILED py/test/unit/rotation_test.py::test_construct_to_output_consistency_euler[quaternion]
    FAILED py/test/unit/rotation_test.py::test_construct_to_output_consistency_euler[matrix]
    FAILED py/test/unit/rotation_test.py::test_construct_to_output_consistency_quaternion[matrix]
    FAILED py/test/unit/rotation_test.py::test_construct_to_output_consistency_matrix[quaternion]
    FAILED py/test/unit/rotation_test.py::test_construct_to_output_consistency_matrix[euler]

What you don't see here is the absurd amount of log spam I created for
myself... we'll let that one blow away into the sands of time.

# Simplify Doesn't Scale

Something in Sympy's implementation of the 
[`simplify`](https://docs.sympy.org/latest/modules/simplify/simplify.html#simplify)
function leads to excessive runtimes for my development machine (on the order
of 300 seconds / 5 minutes). I suspect it's a loop of iteratively making small
changes, then re-evaluating everything on the small change. This is the second
time (or maybe third?) that I've wanted to include simplification into the
project and each time I manage to wander into a case where it's performance is
a hard block on its usefulness. I love Sympy and want to love simplify, so it
seems like something of an outlier to run into a performance issue like this.
