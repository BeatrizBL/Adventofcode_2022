# Day 15: Beacon Exclusion Zone

Description of the task for this day can be found in https://adventofcode.com/2022/day/15.

## Solution used

When looking at the input file, we can see that it contains few sensors, but their coordinates are really large, ranging over several millions. Therefore, it would not be possible to represent the whole matrix. To decide how much of a row a sensor covers, we split its Manhattan distance into the vertical distance from the sensor to the row and then the horizontal remain (to each side).

For part 1, as visible in the commit history, the initial implementation used sets to represent all the positions within an interval covered by a sensor. However, those sets may contain millions of entries. For part 2, the same execution had to be ran 4 million times, so the initial implementation was too slow. In order to identify which part of the code could be optimized, we used native Python profiler `cProfile`. Below we can see part of the output.
```bash
>> python -m cProfile 15_Beacon_Exclusion_Zone/beacon_exclusion_zone.py

4945 function calls (4850 primitive calls) in 5.247 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1009(_handle_fromlist)
        2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:103(release)
        ...
        1    0.000    0.000    0.000    0.000 _bootlocale.py:33(getpreferredencoding)
        1    0.043    0.043    5.247    5.247 beacon_exclusion_zone.py:1(<module>)
        1    0.000    0.000    0.001    0.001 beacon_exclusion_zone.py:27(process_input)
       22    4.812    0.219    5.202    0.236 beacon_exclusion_zone.py:33(covered_positions_in_row)
        1    0.000    0.000    0.760    0.760 beacon_exclusion_zone.py:52(count_not_beacon_positions_in_row)
        1    0.000    0.000    0.000    0.000 beacon_exclusion_zone.py:54(<listcomp>)
        1    0.000    0.000    4.442    4.442 beacon_exclusion_zone.py:56(find_distress_beacon)
      489    0.000    0.000    0.000    0.000 beacon_exclusion_zone.py:6(manhattan_distance)
       24    0.000    0.000    0.001    0.000 beacon_exclusion_zone.py:9(break_down_line)
        1    0.000    0.000    0.000    0.000 codecs.py:260(__init__)
        ...
        2    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
       24    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
       92    0.390    0.004    0.390    0.004 {method 'union' of 'set' objects}

```
In the very last line it shows that the set union is one of the few functions that requires significant time to run (greater than 0). Therefore, the code was changed to store only the start and end values of each interval. The union of two intervals is done manually by comparing the limits in the final implementation. This change was enough for the code to run in less than a minute.
