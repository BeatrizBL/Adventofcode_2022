# Day 25: Full of Hot Air

Description of the task for this day can be found in https://adventofcode.com/2022/day/25.

## Solution used

The proposed number notation is reminiscent of Roman notation. 

To transform from SNAFU notation to decimal it is the same procedure as to change from binary to decimal.

Going from decimal to SNAFU is a bit more complex. The first step is the same as going from decimal to base 5 notation. Then numbers over 2 need to be adjusted to subtract form the higher power. In that case, one unit is added to the next power and numbers are adjusted over a loop. In order to know how long the final number will be, you can use logarithm of base 5.
