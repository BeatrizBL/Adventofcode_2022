# Day 2: Rock Paper Scissors

Description of the task for this day can be found in https://adventofcode.com/2022/day/2.

## Solution used

The rules of the game can be represented as a circular list, with each element winning over the previous one. We use Modulo operator to compare the element indexes in the list.

The output of each match is represented using 1x2 notation: 1 for win, x for draw, 2 for loss.