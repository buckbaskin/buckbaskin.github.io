---
Title: FormaK Runtime - New FormaK Feature
Category: Building
Tags: FormaK, Project FormaK, Python, C++
Date: 2023-08-04
Updated: 2023-08-06
Summary: A new feature for FormaK has landed: The FormaK runtime. The first tool in the runtime is a Managed Filter that handles coordinating process and sensor updates.
---

FormaK aims to combine symbolic modeling for fast, efficient system modelling
with code generation to create performant code that is easy to use.

The new feature provides an extension to the fifth of the Five Keys "C++
interfaces to support a variety of model uses" and "Python implementation of
the model and supporting tooling" by simplifying how Kalman Filters are managed
into a single interface.

After the original [Python design](blog/formak-python-code-generation.html)
and 
[C++ design](https://github.com/buckbaskin/formak/blob/main/docs/designs/cpp_library_for_model_evaluation.md),
the EKF interface from the library provided the wrappers around the math for
updating the state and variances and code generation to implement the models
but not much else. The code to run the filter looked something like:

    double process_dt = options.reading_dt_base + 0.05 - currentTime;
    combined = ekf.process_model(process_dt, combined, control);
    currentTime = currentTime + process_dt;

    featuretest::Simple zero_sensor_reading(SimpleOptions{});
    combined = ekf.sensor_model(combined, zero_sensor_reading);

    process_dt = options.reading_dt_base + 0.06 - currentTime;
    combined = ekf.process_model(process_dt, combined, control);
    currentTime = currentTime + process_dt;

    featuretest::Simple one_sensor_reading(SimpleOptions{});
    combined = ekf.sensor_model(combined, one_sensor_reading);

    process_dt = options.reading_dt_base + 0.07 - currentTime;
    combined = ekf.process_model(process_dt, combined, control);
    currentTime = currentTime + process_dt;

    featuretest::Simple two_sensor_reading(SimpleOptions{});
    combined = ekf.sensor_model(combined, two_sensor_reading);

    process_dt = options.output_dt - currentTime;
    combined = ekf.process_model(process_dt, combined, control);
    currentTime = currentTime + process_dt;

To simplify the interface down to the essential, a new class was created: the
`ManagedFilter`. This provides a single tick interface to handle both process
updates and sensor updates.

    mf.tick(options.output_dt, control,
            {
                mf.wrap<Simple>(options.reading_dt_base + 0.05,
                                SimpleOptions{}),
                mf.wrap<Simple>(options.reading_dt_base + 0.06,
                                SimpleOptions{}),
                mf.wrap<Simple>(options.reading_dt_base + 0.07,
                                SimpleOptions{}),
            });

The ManagedFilter supports both FormaK-generated and non-FormaK implementations
of a Kalman Filter.

Check out the [code](https://github.com/buckbaskin/formak/pull/17) or get the
latest updates for FormaK on [Github](https://github.com/buckbaskin/formak).

## SFINAE

One area of the filter that I'm proud of is the C++ foo I had to sort out to
get the feature working. The ManagedFilter class doesn't use any code
generation, but it does interface with generated code from the C++ generation
of the Extended Kalman Filter. This means that it needs to deal with both
interfaces that have a `Control` and `Calibration` type and interfaces that
have only one or neither.

In C++, a pattern called
[SFINAE](https://en.cppreference.com/w/cpp/language/sfinae) or Substitution
Failure Is Not An Error can be used to achieve this interface without code
generation. At a high level, the idea is to template the members of the class
(even if they otherwise wouldn't require a template) so that when the type is
substituted into the template it can pass (and become part of the interface) or
fail (and not be a part of the interface) based on the filter implementation it
supports.

Getting the details of SFINAE to work was a large chunk of the time spent on
the feature, but in the end I think I've achieved a reasonable solution to the
problem and something I can build on and extend for future features. That said,
I am only cautiously optimistic I could extend the SFINAE approach further
becuase it could become too verbose or go beyond my understanding of how to
make it work. We shall see.

# What's next?

## Filter Improvements

A design for adding innovation filtering is coming soon...

## Improved Netcode

With the manipulation of the process updates and sensor updates wrapped into a
neat single interface, additional improvements can be made. For example, it
becomes easier to optionally include rollback "netcode" into the ManagedFilter
to better handle out of order sensor updates.

In the current system, if a sensor reading comes in from before output time of
the previous tick, the process update is used to go back in time to that sensor
reading before returning forward in time to the new tick time. This adds
additional variance that isn't strictly necessary due to exta use of the
process update.

With rollback, a history of recent states can be saved and then played forward.
For the sensor reading earlier in time, the state would be rolled back to
before this sensor reading, then played forward along with interim sensor
readings to provide the lowest variance estimate of the state by recreating a
monotonically ordered timeline of sensor updates. This approach adds compute
overhead and memory overhead for storing and re-running sensor data, sensor
updates and process updates but promises the best possible estimator accuracy.
