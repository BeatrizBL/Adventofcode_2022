# Day 7: No Space Left On Device

Description of the task for this day can be found in https://adventofcode.com/2022/day/7.

## Solution used

We use a tree structure to represent the file system. Nodes of the tree contain a value to represent the file size. Another FileSystem class is created on top of the Tree class (available in graph.py) to deal with specific requirements, like tracking the current directory.

The size of each directory is computed as the sum of sizes of all its child nodes. Recursive methods are used when needed to move down or up the tree structure.
