# Day 11: Monkey in the Middle

Description of the task for this day can be found in https://adventofcode.com/2022/day/11.

## Solution used

For the first part we create two classes:
- Item, to store the worry level and deal with the increases and reductions in worry.
- Monkey, to store the `queue` of items, perform the item inspections and decide to which monkey throw each item.

The most interesting bit of this part is how to automatically process the input text to define test methods. An input string like `'new = old + 8'` should be transformed into a callable. `eval` method is used for that, together with anonymous functions: 
```python
f = lambda old: eval('old + 8')
new = f(old=2) # >> 10
```

For the second part, the process is repeated so many times that the resulting worry integers are too large for the computer to process. The trick here is to realize that the only operation performed is to check whether the worry level of an item is divisible by a number, which is different for each monkey. Therefore, all worry levels can be trimmed to **the remainder of dividing the worry level by the Least Common Multiple of all monkey check values** (which can be done using the Modulo operator `%`). 
