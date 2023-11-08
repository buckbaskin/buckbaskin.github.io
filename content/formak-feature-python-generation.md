---
Title: FormaK: Python Code Generation
Category: Building
Tags: FormaK, Project FormaK,30 for 30, Code Generation, Python, Sympy
Date: 2022-10-05
Updated: 2023-10-30
Summary: The second feature for FormaK landed: generating Python models
---

Parent Design: [designs/formak_v0.md](https://github.com/buckbaskin/formak/tree/master/designs/formak_v0.md)

# Overview

FormaK aims to combine symbolic modeling for fast, efficient system modelling
with code generation to create performant code that is easy to use.

The values (in order) are:

- Easy to use
- Performant

The Five Key Elements the library provides to achieve this (see parent) are:

1. Python Interface to define models
2. Python implementation of the model and supporting tooling
3. Integration to scikit-learn to leverage the model selection and parameter tuning functions
4. C++ and Python to C++ interoperability for performance
5. C++ interfaces to support a variety of model uses

This design provides the initial implementation of second of the Five Keys
"Python implementation of the model and supporting tooling". This design also
prepares for the third of the 5 Keys: "Integration to scikit-learn to leverage
the model selection and parameter tuning functions". At this stage it is
helpful to inform the design of the tooling so that it won't have any big
hurdles to the next steps in the design.


# Solution Approach

The basic step for this feature is translating from Sympy to Python (without a
sympy dependency). Sympy provides this functionality already, so getting the
basics working wasn't too hard. The follow on work to refactor will be
important in order to make sure that the library remains easy to use.

The key classes involved are:

- `ui.Model`: User interface class encapsulating the information required to define the model
- `py.Model`: (new) Class encapsulating the model for running a model efficiently in Python code

## Tooling

Along with the `py.Model` encapsulation, the code generation tooling provides
an Extended Kalman Filter implementation to quantify variance (based on best
fit of a Kalman Filter to data) and outliers (innovation as a function of
variance). This part of the design is more focused on being used with the
coming scikit-learn integration.

The key classes involved are:

- `py.Model`: (new) Class encapsulating the model for running a model efficiently in Python code
- `py.ExtendedKalmanFilter`: (new)
	- Looking ahead to model fitting, characterize model quality, data variance by fitting an EKF
	- Constructor accepts state type, state to state process model (as a `ui.Model`), process noise, sensor types, state to sensor models and sensor noise
	- Process Model Function: take in current state, current variance, dt/update time. Return new state, new variance
	- Sensor Model Function: take in current state, current variance, sensor id, sensor reading

These two classes will likely share a lot under the hood because they both want
to run Python efficiently; however, they'll remain independent classes to start
for a separation of concerns. The EKF class at this point is more aimed to
using it under the hood of the scikit-learn stuff whereas the `py.Model` class
is aimed at the Formak User (easy to use first, performant second).


## The Cherry On Top - Transparent Compilation

In addition to merely repackaging the model defined in the `ui.Model`, this
design integrates with Python compiler tooling
([Numba](https://github.com/numba/numba)) to write Python in the `py.Model`
class, but JIT compile high use model functions.

This has some trade-offs (increased implementation complexity, increased
startup time), but should likely also have some performance benefits especially
for longer-running analysis use cases (e.g. running with a long sequence of
data). Numba was selected because it could easily be adapted to work with the
generated code, whereas some other compilers (for example Cython) require code
annotation or other changes that would be more involved than I wanted to pursue
at this stage.

### Notes

- In the spirit of don't pay for what you don't use, the compiler option motivated the creation of a common configuration pattern. We want to be able to (at conversion time) selectively enable or disable the compilation. Continuing to put thought into a common configuration pattern will make it easier to reuse in future designs (e.g. selecting configuration about other model optimizations)
