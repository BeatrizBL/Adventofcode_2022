# Day 5: Supply Stacks

Description of the task for this day can be found in https://adventofcode.com/2022/day/5.

## Solution used

The main difficulty in this challenge is to properly process the input data. 

For the stacks:
- Lines are processed using the fact that each crane is always represented by exactly 3 characters. 
- Stacks are implemented using lists, using the `append` and `pop` methods to move elements across stacks.
- The last line is used to identify how many stacks we need to initialize.

For movements:
- Each of the three numbers in the movement are extracted using `regex` (`re.search` method).
