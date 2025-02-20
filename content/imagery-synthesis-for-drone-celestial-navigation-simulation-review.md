---
Title: Imagery Synthesis for Drone Celestial Navigation Simulation, A Review
Category: Building
Tags: Research, Celestial Navigation, Drone, Paper Review
Date: 2025-02-19
Updated: 2025-02-19
Summary: Research notes for exploring celestial navigation
---

Citation: Teague, S.; Chahl, J. Imagery synthesis for drone celestial navigation simulation. Drones 2022, 6, 207.

This paper was cited for imagery generation in the strapdown celestial
navigation paper (
[topic exploration]({filename}/celestial-navigation-for-drones.md),
[review]({filename}/affordable-vision-based-strapdown-celestial-navigation-review.md))

https://doi.org/10.3390/drones6080207

# Star Catalog

> A star catalog must be used as a reference for the location of stars. While there are many star catalogues available, we selected the Yale Bright Star Catalogue (BSC) due to its minimal size. The BSC contains records of stars down to magnitude 6.5, totalling 9110 stars. This magnitude threshold is sufficient for most aircraft camera systems (including stabilized systems) [1]. For ease of implementation, the ASCII-format catalogue was converted into an SQLite database.

My takeaway from this is that I can probably start with a simpler star catalog
(Yale Bright Star) instead of [HYG](https://astronexus.com/projects/hyg) (which
incorporates the Yale catalog.

# Initial Corrections

> On initialization, adjustments are made for the right ascension and declination of stars due to annual proper motion (the apparent motion of stars), precession (changes in the Earth’s rotational axis over time), nutation (axial changes due to the Moon’s gravitational pull) and aberration (due to the velocity of the Earth’s orbit).

This is interesting information that I wouldn't have thought about. I wonder if
this type of correction can be performed once for an online application or
skipped entirely and incorporated into a noise model. It seems like something
I'd definitely want to include when building a batch online system.

There's also a large number of units floating around, so a type system of
measurement seems like it'd be useful for correctness (e.g. arcseconds, Julian
centuries, degrees, etc)

> The observed elevation of a celestial body is altered due to the effects of atmospheric refraction. Consequently, objects in the sky appear at a greater elevation than they would without the atmospheric effects. This effect is exaggerated at lower elevations (closer to the horizon), which leads to an angular displacement of up to 0.5 degrees

# Attitude

Project stars to the aircraft North-East-Down (NED) frame, then rotated by the
aircraft's rotation matrix relative to NED. Maybe more correctly, it's rotated
into the camera's frame. 

# Camera Model

The model assumes a camera intrinsic matrix K is known. This seems reasonable
given that the camera can be calibrated on the ground before launch. Earlier
on, the camera extrinsics relative to the aircraft were also given. This seems
like something that could be calibrated, but would be subject to vibration or
other errors in a real application.

Open question: how feasible is it to estimate camera intrinsics online in a
strapdown visual inertial odometry system?

    TFT [interesting papers but none covering camera intrinsic calibration or estimation]
      (0.590) RoNIN: Robust Neural Inertial Navigation in the Wild: Benchmark,
      Evaluations, and New Methods http://arxiv.org/abs/1905.12853v1
      Preview:
        This paper sets a new foundation for data-driven inertial navigation research, where the task is the estimation of positions and orientations of a mov...
    
      (0.581) Pluto: Motion Detection for Navigation in a VR Headset http://arxiv.org/abs/2107.12030v2
      Preview:
        Untethered, inside-out tracking is considered a new goalpost for virtual reality, which became attainable with advent of machine learning in SLAM. Yet...
    
      (0.574) Iterative Smoothing and Outlier Detection for Underwater Navigation http://arxiv.org/abs/2109.14220v1
      Preview:
        Underwater visual-inertial navigation is challenging due to the poor visibility and presence of outliers in underwater environments. The navigation pe...
    
    arXiv search -> https://arxiv.org/abs/2201.09170 "Online Self-Calibration for Visual-Inertial Navigation Systems: Models, Analysis and Degeneracy"


Points behind the camera (negative z in the camera frame) are ignored (seems
sensible).

There is a simplified model of atmospheric attenuation that lets you scale all
observations based on the relative intensity of a single reference observation
vs its nominal value in the database. This seems important to pick a reasonable
value (is this covered in the paper), but for my use case I'm not interested in
exactly rendering an image. 

Open question: Instead of aiming for perfect rendering accuracy, could I make
the sky fingerprinting intensity independent? I'm imagining something similar
to making image features rotation independent (perhaps by processing all
intensities into a finite 0 to 1 scale)

    TFT
    (0.522) Compressive Sensing with Local Geometric Features http://arxiv.org/abs/1208.2447v1

Pixel intensities and star sizing are taken from a reference image; however,
the ideal model for a star is a point light source. Noise levels are also taken
from the reference image by masking out stars and then using the remaining
variation to fit a Gaussian

Open question: Would it be helpful to perform some sort of sub-pixel
optimization for star pose? I'm not sure what this would get me for my goal,
but it seems interesting. In the images shown, the scale of stars for an
in-motion exposure seems to blur over multiple pixels anyway, so I don't know
if identifying a sub-pixel is as helpful for this use case

    TFT
    (0.556) Conceptual Design on the Field of View of Celestial Navigation Systems for Maritime Autonomous Surface Ships http://arxiv.org/abs/2408.15765v1


> One may be able to determine an appropriate magnitude threshold for the observability of stars in-flight and bias the calibration towards the brighter stars, which are more likely to be detected.

# Lens Distortion

Lens distortion may also be included in the model. Lens distortion models are typically
non-linear, and expressed as a function of displacement from the principal point. Various
models exist for lens distortion, and should be chosen according to the level of precision
required [18]. If using a lens distortion model, this should be applied after the star is
rendered, so as to capture the resultant eccentricities from the distortion.

Reference 18: Tang, Z.; Von Gioi, R.G.; Monasse, P.; Morel, J.M. A precision analysis of camera distortion models. IEEED 2017, 26, 2694–2704.

# Motion Effects

Spherical linear interpolation between quaternions is used to supersample the
known states to get 5 millisecond time steps, which can be aggregated across
the exposure time to composite a blurred motion

