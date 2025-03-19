---
Title: Why Sports Metrics?
Category: Building
Tags: Project Sports Metrics, Sports Metrics, Python, Visualization, Ultimate Frisbee
Date: 2025-03-18
Updated: 2025-03-18
Image: img/heart_rate_map_2025-03-18_22-55-13.jpg
Summary: I've been tracking my training and ultimate frisbee games for some time now, and I recently decided to turn that into something of an adjacent project for attempting to develop metrics to quantify my performance. The initial motivation stems from watching a lot (a lot!) more Premier League soccer and starting to learn more about how high level soccer teams track their players to quantify statistics. Some metrics are out of my league, but some are much more attainable. For example, I can implement metrics such as: Total Distance covered, Sprint Distance, Power, and Top Speed. 
---

I've been tracking my training and ultimate frisbee games for some time now,
and I recently decided to turn that into something of an adjacent project for
attempting to develop metrics to quantify my performance.

The initial motivation stems from watching a lot (a lot!) more Premier League
soccer and starting to learn more about how high level soccer teams track their
players to quantify statistics. Some metrics are out of my league 
(e.g. [expected goals/xG](https://footystats.org/england/premier-league/xg),
but some are much more attainable. For example, the product 
["CatapultOne"](https://www.youtube.com/@catapultone206/videos) advertises
metrics such as:

- Total Distance covered
- Sprint Distance
- Power
- Top Speed

I figured I could take some of these metrics ideas and build on them to create
my own sports metrics.

# A Step in A Direction

I had initially jumped into the complicated, trying to build a mapping from
speeds and accelerations to heart rate. This has promise because it would allow
for comparing heart rate in the same situation (and I'd like to find it to be
lower) or finding that I could access new regimes as my performance improved.

![2D histogram type plot. Darker green indicates higher heart rate](img/heart_rate_map_2025-03-18_22-55-13.jpg)

Here's one example, showing lower heart rates in yellow and higher heart rates
in green. Missing data is shown in purple. Some of this shows the trend of
higher acceleration correlating to higher hear rate, but the relationship isn't
clear (and I think I may have not made the bins intuitive sizes).

I found that I couldn't capture the relationship from that alone because heart
rate has a longer history than just the current motion. I haven't found a data
to support a specific model, but my mental model is that heart rate is a moving
window filter over the speed and changes in direction in the last few seconds
to last few minutes. The intuition is pretty simple. If you're running faster,
your heart rate should be higher. If you've had to change direction more, your
heart rate should be higher. If you've run more in the last time window than
been stopped, your heart rate should be higher.

To find this relationship, I recast the data as a sequence of time windows of
speed and acceleration, then used a linear model to attempt to estimate heart
rate. X is velocity and acceleration from a time window, y is heart rate. Call
scikit-learn fit methods and, bam, profit.

This was promising for many cases, but consistently fell down at the
tails of the distribution. My hypothesis is/was that the data over-samples from
low heart rate cases and low speed cases because a frisbee game is not a long
continuous run, but bursts of points and bursts of motions within the points.
Much of the data for the naive linear regression approach is sourced 

- Aside: As I'm writing this, I think I can take an approach to weight points by an inverse of the density of nearby samples (or proportional to the distance to nearby samples) to achieve a rebalanced approach that's roughly uniform across heart rates.

Ultimately, this was a step in a promising direction, but it was a step in a
complicated direction and I lost momentum on implementing this approach

# A New Direction, A Smaller Step

To get back on track, I've taken steps to build from simpler composable
building blocks and starting small. I've also recently built in some
functionality to automatically produce some more images to show results along
the way.

For example, when looking at active time (or in this case, a histogram of

speeds from a game) there is an obvious bimodal pattern with a strong peak at
zero speed, then a distribution of speeds for in motion.

![Histogram of active time with most samples at zero speed and a small peak at 0.8 and 1.4 meters per sec]({attach}/img/active_time_2025-03-18_22-30-16.jpg)

Building on the concept of active time, I also wanted to track how much
distance I cover as a measure of work rate. This is interesting within a game
(I expect to see decreasing peak work rate over a game) as well as across
games. Soem may have less intensity, some more, but I'd like to see an
increase in peak work rate over time.

![Line plot of speeds with many sharp peaks in blue, with a moving-average overlaid in orange]({attach}/img/work_rate_2025-03-18_22-38-11.jpg)

Building on these, I'll be sharing some additional posts with new
visualizations and new builds
