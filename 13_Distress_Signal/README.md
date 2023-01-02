# Day 13: Distress Signal

Description of the task for this day can be found in https://adventofcode.com/2022/day/13.

## Solution used

In order to create the actual lists from the input strings, recursion is used. The same decoding function is called each time a new list start is detected in the string. A recursive method is also used to check whether the two lists are in the correct order, calling the recursive method when an element of the list is a list itself.

For the second part we need to sort the list of packages. The sorting algorithm named "Bubble Sort" is selected for the task, since it is simple to implement and easily allows comparisons of not numerical elements.
