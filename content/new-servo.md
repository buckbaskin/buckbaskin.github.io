---
Title: What's in a stepper?
Date: 2018-07-19
Category: Breaking
Tags: stepper motor, reverse engineering
---

For a lot of my life, the robots I worked with were pretty close to what CS wants from them: a stream of sensor data in, nicely organized in a common format across all sensors. To make things happen, I stream some outputs in another selection of formats. The sensor data changes and I repeat the loop. (Thanks ROS! It's pretty great and you should check it out.) While having an understanding of the dynamics of the robot and how each sensor generated its reading was helpful, most of that got summed up as: add some extra variance to the Kalman filter and we'll be ok. What happens if you want to get a little more involved in the hardware?

In an attempt to figure that out by breaking something on the path to building. I found a couple of stepper motors I could throw at an Arduino and see what happened.

The first thing that I was surprised by was the variety of stepper motors available, and the fact that I need to decide between a unipolar and bipolar motor before I even knew what I was doing. In practice, there are probably more differences, but what it came down to for me was that there were either 5 or 6 wire variants. What came to me in the mail was 6 wires, so steppers are 6 wires for now.

This [website](http://www.jasonbabcock.com/computing/breadboard/unipolar/index.html) proved immensely useful in the first above the fold section (I got excited and didn't read further but the rest of it is probably also good). I got my hands on a multimeter too! The general principle behind the system is that there are two different wiring loops. They are disconnected, so the resistance between the two sides are infinite. Besides that, the resistance across two steps sums up, so you can place which side should be which (with some directional ambiguity which I figure out later).