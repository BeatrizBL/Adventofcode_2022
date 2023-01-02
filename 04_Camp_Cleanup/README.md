# Day 4: Camp Cleanup

Description of the task for this day can be found in https://adventofcode.com/2022/day/4.

## Solution used

Each interval string is transformed into a binary representation of the positions covered by the interval. For instance, 2-4 is represented as `0000001110`, or 6-8 is `0011100000`. In order to transform those strings into actual binary values, we use `int('0000001110', base=2)` (which corresponds to integer 14). 

Then, `AND` operator is applied to two such integers to identify the overlapping part.
