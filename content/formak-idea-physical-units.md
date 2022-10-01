---
Title: FormaK User Interface - Physical Units as Python Types
Category: Building
Tags: FormaK, User Interface, 30 for 30
Date: 2022-10-03
Updated: 2022-10-01
Summary: Using Python's type checking to check for mismatched physical quantities
---

# The Idea

As part of the FormaK library, I'd like to introduce the concept of physical
units into the UI this would allow for checking that things like the following
are correct (every element added together ends up in units of velocity)

`vel = accel * dt + snap * (dt ^2) / 2`

and something like the following is incorrect (there's a missing dt element)

`position = velocity + position`

# The Hypothesis

I'd also like to approach the integration of units in a "zero-cost abstraction"
way where a user doesn't pay for what they don't use but they do get increasing
utility with increasing effort to use features in the library. This means that
a gradual approach like is used in Mypy/Pep 484 for typing and checking Python
programs would be ideal. In fact, can we take that approach to develop a
physical units system based on Python's types?

# The Experiment

[source](https://github.com/buckbaskin/formak/blob/physical-units-demo/demo/src/physical_units.py)

```python
# ... some hacky code ...

class UnitMeta(type):
    def __getitem__(cls, key: Tuple[int, int]):
        meters, seconds = key
        env = dict(UnitImpl.__dict__)
        env["meters"] = meters
        env["seconds"] = seconds

        Type = type("Unit", (UnitImpl,), env)
        return GenericAlias(Type, key)


class Unit(UnitImpl, metaclass=UnitMeta):
    def __add__(self, rhs: Unit):
        return super().__add__(rhs)


dt = Unit[0, 1]("dt")  # Unit[0,1]
accel = Unit[1, -2]("accel")  # Unit[1,-2]
jerk = Unit[1, -3]("jerk")  # Unit[1,-3]

print("a", accel)
print("dt", dt)
print("a * dt", accel * dt)

vel = accel * dt + jerk * (dt * dt) / 2
print("vel", vel)

position = Unit[1, 0]("position")  # Unit[1,0]

position = (
    vel + position
)  # Expect to fail here (velocity not the same units as position)
```

Mypy command: `python3 -m pip install -U mypy typing; mypy physical_units.py`

Mypy "error" message: `Success: no issues found in 1 source file`

Unfortunately, at this time I've not been able to get to a point where I can
get Mypy to fail with crossing up meters/seconds units.

# The Runtime Checking Future

As a final step to be most useful for FormaK, I'd like to be able to check at
runtime so we can perform the checking as part of model validation. The tool
for the job is [Typeguard](https://github.com/agronholm/typeguard).

Originally I'd expect to be able to use Mypy, but it's pretty set on being a
command line tool for files according to [Guido Van Rossum](https://github.com/python/mypy/issues/2369#issuecomment-256984061):

> ... We're reluctant to make mypy importable and callable from other code, because mypy's primary usage is through the command line, targeted at whole programs, and we often make big changes to the internals that would break external invocations. Think of mypy as a linter ...

However, that redirected me to [Dynamic PEP 484 type checking without code
changes?](https://github.com/python/typing/issues/310)
and that pointed me to Typeguard [[commit](https://github.com/agronholm/typeguard/commit/69ce354d74b9de0cee0efc1b6509e8bb2e51ca47), [User Guide](https://typeguard.readthedocs.io/en/latest/userguide.html)]

Taking another look at the code example above, this time with Typeguard

# Conclusion

This simple example of units focuses on two units (distance, time) and needs
something extra to get working via Mypy type checking. If you'd like to
contribute this or another feature to the FormaK project, reach out to me on
Twitter @bebaskin or reach out on the proposal issue on Github.

