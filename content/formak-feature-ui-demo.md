---
Title: FormaK: User Interface
Category: Building
Tags: FormaK, User Interface, 30 for 30
Date: 2022-10-04
Updated: 2022-10-01
Summary: The first feature for FormaK landed: the user interface!
---

Parent Design: [designs/formak_v0.md](https://github.com/buckbaskin/formak/tree/master/designs/formak_v0.md)

# Overview

FormaK aims to combine symbolic modeling for fast, efficient system modelling
with code generation to create performant code that is easy to use.

The values (in order) are:

- Easy to use
- Performant

In line with those values, the intended user experience is as follows. The user
provides:

- Model that describes the physics of the system
- Execution criteria (e.g. memory usage, execution time)
- Time series data for for the system

And the user gets a performant model that satisfies their execution criteria and
optimally fits the data.

The Five Key Elements the library provides to achieve this user experience are:
1. Python Interface to define models
2. Python implementation of the model and supporting tooling
3. Integration to scikit-learn to leverage the model selection and parameter tuning functions
4. C++ and Python to C++ interoperability for performance
5. C++ interfaces to support a variety of model uses

This feature provides the first of the Five Keys: the Python Interface to define models.

# Feature Preview

The user interface is designed to be easy to use and familiar to folks that
work with Python. Setting up a very simple physics model for a rocket looks
like:


    vp = vehicle_properties = {k: Symbol(k) for k in ["m", "x", "v", "a"]}
    fuel_burn_rate = Symbol("fuel_burn_rate")

    state = set(vehicle_properties.values())

    control = set([fuel_burn_rate])  # kg/sec

    # momentum = mv
    # dmomentum / dt = F = d(mv)/dt
    # F = m dv/dt + dm/dt v
    # a = dv / dt = (F - dm/dt * v) / m

    F = -gravitational_force(vp["m"], Earth_Mass, vp["x"] + Earth_Equatorial_Radius)

    state_model = {
        vp["m"]: vp["m"] - fuel_burn_rate * dt,
        vp["x"]: vp["x"] + (vp["v"] * dt) + (1 / 2 * vp["a"] * dt * dt),
        vp["v"]: vp["v"] + (vp["a"] * dt),
        vp["a"]: (F - (fuel_burn_rate * vp["v"])) / vp["m"],
    }

    orbital_model = Model(dt=dt, state=state, control=control, state_model=state_model)


Based on [orbital_test.py](https://github.com/buckbaskin/formak/tree/master/featuretests/python_ui_demo/orbital_test.py)

One of the areas that I'm working on improving further is the way to set up
symbols. In a very complicated system, having to specify everything in a
verbose way isn't necessarily sustainable.

# Solution Approach

To start, the user interface leans on the
[`sympy`](https://www.sympy.org/en/index.html) package for symbolic math. Sympy
shares the value of being easy to use. In addition to the values match, leaning
on sympy instead of a proprietary interface enables a lot of flexibility and
future progress for things like code generation based on the model. 

This feature is ultimately simple because it leaned on `sympy` quite a
bit. The primary change from the first plan was that there was already demo
code to borrow from for feature tests which made writing them much quicker.

# Roadmap and Milestones

The development process for this feature and future features follows:

1. Design Doc
2. Write feature tests. When the feature tests pass, the feature is nominally working at an alpha level
3. Build a simple prototype
4. Implement the feature, including additional testing
5. Code Review, Refactor
6. Merge via PR
7. Write up successes, retro of what changed (to include that feedback in future designs)

