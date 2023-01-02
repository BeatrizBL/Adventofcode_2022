# Day 12: Hill Climbing Algorithm

Description of the task for this day can be found in https://adventofcode.com/2022/day/12.

## Solution used

The map is processed into a directed graph. Each `(i,j)` position is connected to the nearby positions whose height is reachable from the current node. 

In order to easily compare heights, the a-z values are transformed to integers using the ASCII representation of each letter with `ord`.
