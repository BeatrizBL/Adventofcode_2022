# Day 3: Rucksack Reorganization

Description of the task for this day can be found in https://adventofcode.com/2022/day/3.

## Solution used

The list manipulation steps are split into simple, independent methods that are called as a pipeline using `reduce` method from `functools` package.

In order to compute the priority of each letter, their ASCII representation is used to obtain an integer (`ord` method).
