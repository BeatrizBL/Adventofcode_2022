from helpers import read_file_into_list, compute_least_common_multiple, process_direction, manhattan_distance
from priority_queue import PriorityQueue
import numpy as np


class Valley():

    def __init__(self, valley_input: list):
        self.height = len(valley_input) - 2
        self.width = len(valley_input[0]) - 2
        self.border_char = '#'
        self.empty_char = '.'
        self.blizzard_char = 'B'
        self.blizzards = self.process_blizzards(valley_input)
        self._states = None

    def process_blizzards(self, valley: list) -> list:
        blizzards = []
        for i, s in enumerate(valley[1:-1]):
            s = s.replace(self.border_char,'')
            for j, c in enumerate(s):
                if c != self.empty_char:
                    blizzards.append((c, (i,j)))
        return blizzards

    def mark_valley(self, blizzards: list = None) -> np.array:
        valley = np.array([[self.empty_char]*self.width for _ in range(self.height)])
        blizzards = blizzards if blizzards is not None else self.blizzards
        for _, (i,j) in blizzards:
            valley[i,j] = self.blizzard_char        
        return valley
    
    def _adjust_position(self, position: tuple, direction: str) -> tuple:
        i, j = position
        if direction in ['^', 'v']:
            return (0 if direction=='v' else self.height-1, j)
        if direction in ['>', '<']:
            return (i, 0 if direction=='>' else self.width-1)
        
    def is_valid(self, position: tuple):
        i,j = position
        return i >= 0 and i < self.height and j >= 0 and j < self.width
        
    def move_blizzard(self, position: tuple, direction: str) -> tuple:
        ni, nj = process_direction(position=position, direction=direction)
        if not self.is_valid((ni,nj)):
            ni, nj = self._adjust_position((ni,nj), direction)
        return (ni, nj)

    def move_blizzards(self, blizzards: list) -> list:
        new_blizzards = []
        for d, (i,j) in blizzards:
            ni, nj = self.move_blizzard(position=(i,j), direction=d)
            new_blizzards.append((d, (ni, nj)))
        return new_blizzards

    def simulate_valley_states(self) -> list:
        cycles = compute_least_common_multiple([self.height, self.width])
        blizzards = self.blizzards
        states = []
        for _ in range(cycles):
            states.append(self.mark_valley(blizzards))
            blizzards = self.move_blizzards(blizzards)
        return states    
    
    @property
    def states(self) -> list:
        if self._states is None:
            self._states = self.simulate_valley_states()
        return self._states
    
    def is_empty(self, position: tuple, state_idx: int) -> bool:
        if not self.is_valid(position):
            return None
        state = self.states[state_idx]
        return state[position] == self.empty_char


def heuristic(position: tuple, exit: tuple) -> int:
    return manhattan_distance(position, exit)

def compute_possible_movements(
    valley: Valley,
    position: tuple,
    state_idx: int
) -> list:
    i, j = position
    possible = [p for p in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)] if valley.is_valid(p)]
    positions = []
    for p in possible + [(i,j)]:
        empty = valley.is_empty(p, state_idx)
        if empty or empty is None:
            positions.append(p)
    return positions

def compute_min_path(
    valley: Valley,
    start: tuple,
    exit: tuple,
    state_idx: int = 0
) -> tuple:
    visited = [] # (position, valley state)
    queue = PriorityQueue()
    queue.add((start, state_idx, 0), (0, heuristic(start, exit), 0)) # (position, valley state, minutes), (minutes, distance, loop step)
    iter = 0
    while not queue.empty:
        position, state_idx, minute = queue.pop()
        next_state_idx = (state_idx+1) % len(valley.states)
        if position == exit:
            return (minute + 1, next_state_idx)
        next_positions = compute_possible_movements(valley, position=position, state_idx=next_state_idx)
        for next_pos in next_positions:
            if (next_pos, next_state_idx) not in visited:
                iter += 1 # To break ties in priority by picking the first added one
                visited.append((next_pos, next_state_idx))
                h = heuristic(next_pos, exit)
                queue.add((next_pos, next_state_idx, minute+1), (minute+1, h, iter))
    return None


if __name__ == '__main__':
    input = read_file_into_list(path='24_Blizzard_Basin/24_input.txt')
    valley = Valley(valley_input=input)

    n1, idx1 = compute_min_path(valley, start=(-1,0), exit=(valley.height-1, valley.width-1))
    answer = n1
    print(f'Answer to part 1: {answer}')

    n2, idx2 = compute_min_path(valley, start=(valley.height, valley.width-1), exit=(0,0), state_idx=idx1)
    n3, _ = compute_min_path(valley, start=(-1,0), exit=(valley.height-1, valley.width-1), state_idx=idx2)
    answer = n1 + n2 + n3
    print(f'Answer to part 2: {answer}')
