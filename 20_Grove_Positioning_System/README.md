# Day 20: Grove Positioning System

Description of the task for this day can be found in https://adventofcode.com/2022/day/20.

## Solution used

Before starting we notice that on the input file there are repeated numbers (3628 unique values vs 5000 total). Therefore, we cannot locate the position of each one on the list based on their value. In order to keep track of where each of the original numbers is, we replace them by an identifier using a dictionary. That identifier is going to be simply their position in the original list.

Once the list is made of unique numbers, we can decide the ending position of the value using the modulo operator. However, there is a trick: since the list is linked, the first and last positions are actually the same. Therefore, 
- we need to compute the modulo with respect to `len(L)-1` instead of simply `len(L)`
- and adjust the position by one before or after when the final position overflows over the "edges".
