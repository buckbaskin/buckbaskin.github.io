---
Title: Working with small gears
Category: Building
Tags: 3D Printing, Additive Manufacturing, Macro
Date: 2020-10-24
Updated: 2020-11-03
Summary: How small can we get with a functional gear part on a FDM printer?
Image: img/IMG_0336.jpg
---

How small can we get with a functional gear part on a FDM printer? At this point, the internal gears for a differential are the limiting factor for designing a 3D printed RC car.

# XMods Differential

Existing XMods use a very compact design that works fairly well; however, it's
hard to take apart without permanently damaging it so I've stuck to replicating
other designs.

![Image]({attach}/img/ExampleDifferential.jpg)

# Right Angle Gears

One of the key elements to replicating the XMods differential is a right angle
drive from a longitudinal motor (or revisiting whether or not a longitudinal
motor makes sense). So far, the right-angle gears haven't come out at a very
high quality, in part because they weren't designed with the extrusion width in
mind. Another avenue of improvement is reducing the gear reduction required
between the drive motor and the differential, which could reduce the number of
teeth required, which would enable more sturdy, easier to print teeth.

![Image]({attach}/img/IMG_0322.jpg)

# Small Gears

When taking into account the width of the extruder, it is easier to get small
gears of various designs to print well. There are opportunities to go down a
step in terms of extruder widths to print an even smaller gear; however, at this
time, I've left some margin in an attempt to have a more reliable print and
hopefully maintain some strength. In the end, gears used in the differential are
responsible for transmitting drive torque from the motor.

![Image]({attach}/img/IMG_0324.jpg)

# Proof of concept differential

These smallest (or nearly minimum size) gears, combined with a printed shaft and
"bushings" (not shown) can enable a fairly compact differential design. The
rendering shown isn't refined to reflect the final input gear (on the left);
however, the internals are close to correct and reflect the layout that I'm
using for testing.

![Image]({attach}/img/ScreenshotDifferential.jpg)

Taking a close look at the gear, it actually has come out pretty well. For
reference, the squares are 10 mm to a side (and straight, the macro lens warps
the image somewhat). At this scale, it was fairly tricky to actually get the
shaft and the gear to press fit together. It took a couple prints to get the
sizing right to get a nice fit without it seeming like it'd slip too much.

![Image]({attach}/img/IMG_0336.jpg)

