---
Title: Strapdown IMU Reference Model - New FormaK Feature
Category: Building
Tags: FormaK, Project FormaK, Python, C++, IMU, Strapdown IMU
Date: 2023-10-29
Updated: 2023-10-30
Image: img/biased_imu_accel_data.jpg
Summary: A new feature for FormaK has landed: the Strapdown IMU Reference model. The model is now available for inclusion into new models and use as a reference for implementing future models.
---

FormaK aims to combine symbolic modeling for fast, efficient system modelling
with code generation to create performant code that is easy to use.

This reference model is an example of the "Python Interface to define models"
which serves two purposes:
1. Provide a reference for implementing a strapdown IMU as a part of other models
2. Further exercise the FormaK interface to sand down rough edges

As a third consideration, this will also provide a reference design for how
other reference models will be designed and presented in the future.

Pull Request: [#19](https://github.com/buckbaskin/formak/pull/19)
Commit: [16ba541](https://github.com/buckbaskin/formak/tree/16ba541e799dfe1b289618a7b27ec48847191172)

# Along The Way

This design has grown in time further than I would have liked. Originally, I'd
aimed for 2 weeks to 4 weeks, and it's now closer to 6.

A few things have stayed the same. The design remains intended to provide a
reference for inclusion in other designs and I was able to learn from some of
FormaK's rough edges. Unfortunately, one aspect (`sympy.simplify` execution
time) cropped up again and I did not reach a suitable resolution.

The few things that have stayed the same are notable because pretty much every
aspect of this design has been adapted from the original.

## Sympy, Quaternions

The math outlined in the original design was largely replaced by using the
Sympy Quaternion model. This was absolutely the correct decision and I should
have done some more research before starting to see if Sympy had this type of
rotation representation already. At latest, this should have been found in the
experimental phase of the project. In the end, ~3 weeks could have been cut out
of the timeline if I'd recognized this at the experimental phase.

## Feature Testing

The feature test was also replaced wholesale. This was partly for convenience
(I already have NASA data) but also because the NASA data comes with clearly
defined motion information. The start of the data is pre-ignition and then
there are also known times for ignition and liftoff. This pre-ignition data
serves as a more test-able feature test because I can know the orientation of
the IMU (provided by the NASA documentation) and perform a pseudo-static test
to assert that the motion of the sensor data doesn't move. This pseudo-static
test made it easy to understand when the model wasn't oriented correctly or
incorrectly accommodating gravity. For example, something is off when there's a
2g (19.62 m/s2) effect in what should be a static test.

The change in feature test also provided the motion for two extensions to the
model beyond the basics: calibration for IMU orientation and calibration for
IMU acceleration biases.

First, the IMU was rotated in all axis away from the nominal navigation frame,
motivating the use of calibration to "remove" this in favor of reporting in
neat and tidy vehicle aligned axis.

Second, the IMU exhibited acceleration bias that quickly caused non-zero motion
even over relatively short time scales (~1 second). Some of the bias could be
corrected, but some was also a random walk that would need to be modeled within
the noise in a full filter implementation and corrected for via fusion with the
onboard LIDAR system.

![Biased velocity data]({attach}/img/biased_imu_vel_data.jpg)

![Biased acceleration data with approximate visual center not at 0, 0]({attach}/img/biased_imu_accel_data.jpg)

## Unit Testing

The design also missed some straightforward opportunities for unit testing.
Specifically, the final implementation has unit tests for static motion and
circular motion that have straightforward closed-form references to compare to
the IMU model.

# What's next?

## Simplify Hyper Mini

I've run into slowdowns with Sympy's `simplify` function in multiple areas of
the projects. I'm going to take a small detour from general feature work to
spend some more time looking into the root cause of poor performance when
simplifying expressions.

## Model fitting

I spent a lot of time in the
[innovation filtering design document](https://github.com/buckbaskin/formak/blob/16ba541e799dfe1b289618a7b27ec48847191172/docs/designs/innovation_filtering.md)
describing the model selection process. Now that I've moved past the refactor
and onto the next thing, I'm looking forward to implementing the automatic
model selection process.
