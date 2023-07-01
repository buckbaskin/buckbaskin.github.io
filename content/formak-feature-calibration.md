---
Title: Calibration - New FormaK Feature
Category: Building
Tags: FormaK, NASA, Rocket Science, Project FormaK, Code Generation, Python, C++
Date: 2023-05-06
Updated: 2023-06-30
Image: img/nasa_flight_sample.gif
Summary: A new feature for FormaK has landed: generating models with calibrated sensors
---

This feature started with a relatively straightforward idea: use FormaK to model
a rocket launch based on NASA data. NASA provides data from a launch in October
2020 with a number of sensors aboard including an IMU, LiDaR and a black and
white camera. The mission collected data to help prototype a lunar lander with a
similar sensor suite.

![Sequence of black and white images of mountainous terrain viewed from the sky]({attach}/img/nasa_flight_sample.gif)

As a first goal, I wanted to model the motion of the rocket via the IMU data by
integrating the IMU as a motion model, with the intent to fuse the IMU data with
LiDaR readings. This runs into the small snag of understanding the orientation
of the IMU and LiDaR with respect to the rocket's coordinate frame. In theory,
the offset and orientation could be estimated online, but the problem is highly
nonlinear for the IMU case and it's not clear to me that online estimation of
the LiDaR calibration is feasible.

Fortunately, the NASA dataset comes with calibration information for the pose
and orientation of the sensors along with other data about how the sensor
information was captured.

Unfortunately, FormaK doesn't support calibration information. FormaK only
supports online control inputs (which could be leveraged to pass in known
information into the state vector, but not sensor models) and online estimated
states.

Fortunately, we can enhance FormaK to support this use case. Inserting
calibration into the mix involved adding it to lots of files; however, its use
is fairly straightforward (no estimation involved, no generated models, just
static values). In addition, the rocket model itself provides a \*good test of
the feature where I can set up the model with the calibration values from NASA
and then iterate until it's working.

Overall, this change was fairly mechanical in nature, but it unlocks a new class
of models that support runtime configuration. This supports the use case of
providing calibration values from NASA's dataset, but the new feature can also
be applied to other areas too. For example, a single model could be defined for
a time of flight ranging system and then multiple instances of the model could
be used by launching them with different calibration parameters.

Check out the code or get the latest updates for FormaK on
[Github](https://github.com/buckbaskin/formak).

# What's next?

One problem I did run into was the templating that underlies the current C++
code generation. Supporting optional calibration terms with the various input
types, function arguments and logical steps made a huge mess of the template
file.

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
            )

This mess felt unsustainable: if I tried to add any additional features or even
change the features I had, this pile of if statements and formatting comments
(and the occasional actual code) needed a different approach.

# 2023-06-25

\* I did find a gap in the original testing of the calibration feature: I had
missed including the calibration in the calculation of the jacobian of sensor
models. This test escape also makes sense in the context of my focus for the
model: process model and IMU data first, all other sensor data second. This
jacobian issue would have been caught if I'd put any meaningful amount of
additional thought into testing the sensor update.
