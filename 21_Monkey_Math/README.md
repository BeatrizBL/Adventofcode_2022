# Day 21: Monkey Math

Description of the task for this day can be found in https://adventofcode.com/2022/day/21.

## Solution used

For part 1 we use a simple recursive function to replace each monkey expression until a number is found. Each time an expression is replaced, we add parenthesis around it to ensure operation order. The final string is evaluated with `eval` method to process the equation.

Part 2 is similar but the value that should be returned by "humn" is replaced by an "x" variable. We end up with an equation with one variable, which is solved using `sympy` equation solver.
