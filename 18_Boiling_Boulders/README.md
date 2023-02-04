# Day 18: Boiling Boulders

Description of the task for this day can be found in https://adventofcode.com/2022/day/18.

## Solution used

For the first part, the class definition is not needed, since it is enough to loop over the cubes. However, part 2 was more complex, so the code was organized in a class. 

As indicated in the description, for part 2 we need to simulate water crawling on the surface of the droplet. Keep in mind that sectioning the figure or traversing it on a straight direction won't work (or would require a pretty complex logic). For instance, if the cubes are set forming a big, empty cube with a small hole on one side.

In order to do that, we "encase" the figure in a bigger cube and, starting on one of the corners of the cube, we expand the search in all possible directions. The expansion is implemented using a queue of unvisited empty space positions, adjacent to the visited ones. Then, for each position of empty space we count how many cubes surround it. 