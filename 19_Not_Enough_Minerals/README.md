# Day 19: Not Enough Minerals

Description of the task for this day can be found in https://adventofcode.com/2022/day/19.

## Solution used

For this problem we will implement a numerical solution instead of the more obvious option of using a graph representation of the possibilities. In order to do that, we will model the problem as a set of inequalities and use the [integer linear programming](https://en.wikipedia.org/wiki/Integer_programming) implementation from `cvxopt` library to find a maximum value. One of the advantages of this approach is that the computation is almost instantaneous.

The variables in the problem, denoted as $Rx_i$ will be the count of robots from type $x$ available at the beginning of minute $i$. That is, we have a total of $24\cdot 4=96$ variables for the first part and $32\cdot 4=128$ for the second part. If we denote as $T$ the total count of minutes (24 and 32 for each part respectively), the formula that we want to maximize is the total count of geodes produced:
$$geodes = Rg_1 \cdot T + Rg_2 \cdot (T-1) + \cdots + Rg_T \cdot 1$$
Variables to count robots from other types have weight 0 in this formula.

Now we need to define the problem as a set of inequalities like $ax + by + ... \leq k$, with all variables on the left-hand side. We use the following set of constrains:

- The amount of robots of each type on each minute is limited by the materials available to build them until that minute. That is, the total amount of materials collected until that point minus the materials used to build other types of robots, divided by the cost. We have to take into account that we start with one ore robot, so we do not need to subtract its cost.  
For example, for geode robots we have the following two inequalities for the first example blueprint. One for ore and the other one for obsidian:

$$
Rg_i \leq {1 \over 2} \left[ \sum_{j=1}^{i-2} Ror_j - \Big( 4 (Ror_{i-1} - 1) + 2Rcl_{i-1} + 3Rob_{i-1} \Big) \right] \quad \longrightarrow \quad
2Rg_i - Ror_1 - \cdots - Ror_{i-2} + 4 Ror_{i-1} + 2 Rcl_{i-1} + 3 Rob_{i-1} \leq 0
$$

$$
Rg_i \leq {1 \over 7} \sum_{j=1}^{i-2} Rob_j \quad \longrightarrow \quad
7Rg_i - Rob_1 - \cdots - Ror_{i-2}\leq 0
$$

- We can build just one robot at each step. That is, the total count of robots is, at most, one more than the previous count.

$$
Ror_{i} + Rcl_{i} + Rob_{i} + Rg_{i} \leq Ror_{i-1} + Rcl_{i-1} + Rob_{i-1} + Rg_{i-1} + 1  \quad \longrightarrow \quad Ror_{i} + Rcl_{i} + Rob_{i} + Rg_{i} - Ror_{i-1} - Rcl_{i-1} - Rob_{i-1} - Rg_{i-1} \leq 1
$$

- It is not possible to lose robots. That is, the count of robots of each type is, at least, the same as in the previous step. For example, for ore robots,
$$Ror_{i-1} \leq Ror_{i} \quad \longrightarrow \quad Ror_{i-1} - Ror_{i} \leq 0$$

- We could add extra inequalities to define the boundaries on the number of robots between 0 and $i$. That would simply reduce the search time, but the execution is already very fast.

We define also the starting conditions (just 1 ore robot) using equalities:
$$Ror_1 = 1, \quad Rcl_1 = 0, \quad Rcob_1 = 0, \quad Rg_1 = 0$$
