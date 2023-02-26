# Day 24: Blizzard Basin

Description of the task for this day can be found in https://adventofcode.com/2022/day/24.

## Solution used

In this case it is pretty simple to compute in advance all the possible states for the occupied positions in the board, since the cycle length is the Least Common Multiple of the width and height of the board. 

We can think of the movement through the board as a graph, where the nodes are a combination of the position in the board and the state of the blizzards. Therefore, if at some point a path leads to a visited position in the board and in the same cycle point of the blizzards, it can be considered as if that state was already visited and the path gets discarded.

To try to speed up the search a bit, we used a version of A* algorithm. You can see more details about this algorithm on day 16. For the heuristic we use the Manhattan distance between the current position and the exit point, which is always going to be (equal or) lower than the actual time needed to reach the exit. However, that heuristic is too simplistic to find the optimum. A better heuristic should also take into account the time needed to reach that position. 

Different linear combinations of the Manhattan distance and the time found different paths. However, after playing with it a bit, we decided to try with an approach closer to Breadth-first search by giving higher weight to the time than to the distance. Although it took significantly longer to run, it found the optimum and still finished in a reasonable time.
