---
Title: Tearing Down a Quadcopter: Part 3 - Reading a Circuit Board
Date: 2018-07-24
Category: Breaking
Tags: quadcopter, multimeter, reverse engineering
Summary: 
Status: Draft
---

My background in electrical engineering involves the first 4 chapters of an
electronics textbook I read on my phone when I had internet connection and power
in town while hiking the Appalachian Trail. What can I figure out about how the
circut board works for the quadcopter?

![Circuit Board Mystery]({attach}img/board_layout.jpg)

First, some easy wins: The motors are marked with a capital M, and the LEDs are
marked with a capital L on the top of the board. I'm guessing this is for
soldering on the leads by hand because there's quite a bit of heat melting away
at the blue top coat. The other easily identified marks on the top of the board
are the B+ and B- for the battery (and charging) leads and an "SK" that appears
to lead to the main power switch via a 2 wire connector.

Another interesting note: The camera connector and the power switch are rigidly
mounted to the quadcopter chasis, so they're actually on their own separate PCB,
probably to reduce the effect that vibration has on the main PCB. The charging
port is essentially the same thing, but its just a connector with a handy little
physical mount connected by some flexing wire to the main board.

I have some hints from my [last article]({filename}break-quad-copter2.md).
I also have some general guidance from this
[handy website](http://www.uchobby.com/index.php/2007/07/15/identifying-electronic-components/)
I found as the second or third google search result. I can see the major
components that are connected off the board, and I can check voltages, but
beyond that I'm on my own (and I have to guess at things like checking for a PWM
signal).

I've also found a less destructive way to look at the bottom of the board by
opening up the battery door, but to really see everything on the bottom of the
board, I'm going to need to take out my handy dandy screw driver and lift the
board of its vibration reduction mounts.

I feel silly, but during this process, I realized that the board has an antenna.
Now you know!