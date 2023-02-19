# Day 22: Monkey Map

Description of the task for this day can be found in https://adventofcode.com/2022/day/22.

## Solution used

Part 1 is pretty simple just by representing the board with a dictionary, similar to previous days.

For part 2, the complex part is to map the out and in paths of each face of the cube. Although there may be a programmatical way to find out the proper folding of the cube, I decided to map it manually and reuse the implementation of part 1. Using the identifiers of each cube face provided in the example, I wrote down the wrapping rules as a dictionary. 

For instance, for A and B points of the example in the description, I defined that by exiting face 4 on the right you enter face 6 facing down. On top of that, I needed to define the order in which the positions of each edge are paired, since in some cases you need to reverse them.
