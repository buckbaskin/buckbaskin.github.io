---
Title: CPU Modeling: First Order Latency and Data Dependencies
Category: Building
Tags: Miniseries, FormaK, CPU, SIMD
Date: 2022-12-01
Updated: 2022-12-01
Summary: This post is a new episode in a miniseries focused on modeling the workings of a CPU to use for generating optimal code. This post focuses on taking a sequence of instructions and simulating their results while respecting the latency of each instruction execution and data dependencies between instructions.
---

This post is a new episode in a miniseries focused on modeling the workings of
a CPU to use for generating optimal code. This post focuses on taking a sequence of instructions and simulating their results while respecting the latency of each instruction execution and data dependencies between instructions.

Skip to [a solution](#a-solution)


# A Solution

[Github PR](https://github.com/buckbaskin/formak/pull/7/files)

The initial solution is fairly simple: partition registers into two categories.
The first categories are registers with data that's available. The instruction
writing to that has completed its full latency and written to the memory
(ignoring different caching for now). The second category are registers with
data that's "in progress". The instruction writing data to that register hasn't
completed yet, so an instruction that depends on the data can't use it yet.

Each in progress register is tagged with the cycle when it'll become available.
This allows the CPU to block on the data dependency if the next instruction to
process depends on data that isn't in the available registers.

## Wide Registers

The first instruction to prototype this operation was just a 4 way element wise
addition. This means that the wide registers of 4x 32bit floats aren't really
that different from a single value; however, this won't always hold. Some SIMD
operations perform custom logic or shuffling for values based on where they are
in the batch.

To allow for this generalization, each operation defines a function for custom
logic that returns a wide register with the correct output values. At the time
the instruction "enters" the CPU and its data is available, the result is
calculated and inserted into the in-progress registers with the correct latency
applied.

## Usage

With a model of latencies and register storage, the "CPU" can run a fixed list
of instructions by continually iterating through the list until all
instructions are consumed and all registers become available. The unsurprising
but happy result of this baby CPU model is that we can see (with a very simple
program) an increase in cycle count for a set of instructions with a data
dependency vs one without a data dependency.

# Missteps

## Throughput

The one big miss for the initial algorithm is accounting for the throughput of
instructions. In a pipeline-based architecture (which covers most CPUs today)
multiple instructions can be in flight at once as long as their data is
independent. The model as written takes a simpler approach and only processes
one instruction at a time, which leads to an under-estimate of throughput for
some cases.

## Register Writing

If two subsequent instructions with different delays write to the same output
register, whichever instruction enters the CPU second will overwrite the result
of the first, potentially shortening or increasing the latency when the value
will be ready and changing its value.

In practice a better approach would allow for different instructions to write
to the same register without overwriting each other. This would allow for a
third instruction to read the first available value and start computation
before the second value gets written into the register.

There's also the chance that what I've written is actually how a processor is
expected to behave, but for now I'll just leave it as a potential bug to
revisit.
