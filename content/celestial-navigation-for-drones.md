---
Title: Celestial Navigation, starting with drones
Category: Building
Tags: Research, Drone, Celestial Navigation
Date: 2025-02-18
Updated: 2025-02-18
Summary: Research notes for exploring celestial navigation
---


Recently, the paper 
["An Algorithm for Affordable Vision-Based GNSS-Denied Strapdown Celestial Navigation"](https://doi.org/10.3390/drones8110652)
came across Hacker News 
([discussion link](https://news.ycombinator.com/item?id=42767797)),


This post is focused on research starting from the paper but focusing on nearby
topics. A separate post will review the paper in more detail 
([An Algorithm for Affordable Vision-Based GNSS-Denied Strapdown Celestial Navigation, A Review]({filename}/affordable-vision-based-strapdown-celestial-navigation-review.md))

Citation: Teague, S.; Chahl, J. An Algorithm for Affordable Vision-Based GNSS-Denied Strapdown Celestial Navigation. Drones 2024, 8, 11.

# Paper References

I found the paper's references to be useful in addition to finding the paper
interesting itself

## The Math

Van Allen, J.A. Basic principles of celestial navigation. Am. J. Phys. 2004, 72, 1418–1424.

This paper was cited for the math for projecting star observations onto the
terrestrial sphere

## Other Celestial Methods

Wang, J.; Chun, J. Attitude determination using a single star sensor and a star density table. J. Guid. Control Dyn. 2006, 29, 1329–1338.

This paper was cited as an example of a space application that uses celestial
positioning for attitude reference

## Simulation

Teague, S.; Chahl, J. Imagery synthesis for drone celestial navigation simulation. Drones 2022, 6, 207.

This paper was used to simulate measurements in the parent paper, including
testing against motion blur effects and testing the effect of wind conditions
on accuracy. My interest comes in learning to create simulated imagery of
celestial bodies for position estimation simulation, which seems like a subset
of the application already covered in the paper. The imagery synthesis also
covers converting a star's database information into the theoretical observed
position


## Star Databases

Wei, X.; Zhang, G.; Jiang, J. Star identification algorithm based on log-polar transform. J. Aerosp. Comput. Inf. Commun. 2009, 6, 483–490.

From the paper: "During the instantiation of the star tracker, a lost-in-space
log-polar star identification algorithm is used to determine the IDs of each
star in the frame". This initialization of the star tracker and generic star
identification seems quite useful to run in a parallel loop as a 
[kidnapped robot](https://en.wikipedia.org/wiki/Kidnapped_robot_problem)
recovery process.

In addition to what's cited by the original paper, I also found a
recommendation for the [HYG Database](https://astronexus.com/projects/hyg)
(also on [Codeberg](https://codeberg.org/astronexus/hyg)). From Codeberg

> HYG combines every identifiable star in the HIPPARCOS, Yale Bright Star, and Gliese (nearby star) catalogs into a combined dataset of the stars' currently best-known positions, brightnesses, spectral types, and various additional catalog IDs such as traditional names and Bayer designations.

# Tools for thought related papers

This content was surfaced by integrating with my own tools that search
arXiv.org to help find interesting and related content.

## History of Celestial Navigation

The beginning of celestial navigation http://arxiv.org/abs/2209.02371v1

## Celestial Navigation System Design

Conceptual Design on the Field of View of Celestial Navigation Systems for Maritime Autonomous Surface Ships http://arxiv.org/abs/2408.15765v1

Orbit Estimation Using a Horizon Detector in the Presence of Uncertain Celestial Body Rotation and Geometry http://arxiv.org/abs/1804.04401v2


## Compressive Sensing for Efficient Representation

Compressive Sensing with Local Geometric Features http://arxiv.org/abs/1208.2447v1

Taking from the abstract:

>  We propose a framework for compressive sensing of images with local distinguishable objects, such as stars, and apply it to solve a problem in celestial navigation. Specifically, let x be an N-pixel real-valued image, consisting of a small number of local distinguishable objects plus noise. Our goal is to design an m-by-N measurement matrix A with m << N, such that we can recover an approximation to x from the measurements Ax. 

This seems like an immediately useful application for finding an efficient
representation of different views of the sky. Without the tool, I was
peripherally aware of compressive sensing, but would not have thought that it
related to my interest in celestial navigation.


CELESTIAL: Classification Enabled via Labelless Embeddings with Self-supervised Telescope Image Analysis Learning http://arxiv.org/abs/2201.08001v1

This paper covers using extensive (petabytes) of unlabelled data to learn a
[compressed] representation of the image class, which feels like it could be
useful for learning a compressed representation of star observations.

## Space Vision Applications

AstroVision: Towards Autonomous Feature Detection and Description for Missions to Small Bodies Using Deep Learning http://arxiv.org/abs/2208.02053v1

This paper seems interesting if a bit off-topic for Earth-based navigation;
however, the visual navigation feels like it would overlap with my other
visual-odometry [research interests]({filename}/research-areas-for-2025.md)

# Additional Special Issue Topics

Paper by the MDPI journal Drones, specifically a special issue on 
[Drones Navigation and Orientation](https://www.mdpi.com/journal/drones/special_issues/uav_navori)



... Written with 
[tools for thought]({filename}/tools-for-thought-and-discovery.md) to help
connect to new ideas I wouldn't have found otherwise
