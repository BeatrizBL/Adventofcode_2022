from helpers import read_file_into_list
from numpy import inf

def process_elves(input: list, elf: str = '#') -> dict:
    elves = {}
    n = 1
    for i, s in enumerate(input):
        for j, c in enumerate(s):
            if c == elf:
                elves[n] = (i,j)
                n += 1
    return elves

def compute_proposed_positions(elves: dict, directions: list) -> dict:
    prop = {}
    current_pos = set(elves.values())
    for elf, (i,j) in elves.items():
        p = None
        adj = [(i-1,j-1), (i-1,j), (i-1,j+1), (i,j+1), (i+1,j+1), (i+1,j), (i+1,j-1), (i,j-1)]
        if any([p in current_pos for p in adj]):
            for d in directions:
                if d == 'N':
                    to_check = [(i-1, j-1), (i-1, j), (i-1, j+1)]
                    prop_next = (i-1, j)
                elif d == 'S':
                    to_check = [(i+1, j-1), (i+1, j), (i+1, j+1)]
                    prop_next = (i+1, j)
                elif d == 'W':
                    to_check = [(i-1, j-1), (i, j-1), (i+1, j-1)]
                    prop_next = (i, j-1)
                else:
                    to_check = [(i-1, j+1), (i, j+1), (i+1, j+1)]
                    prop_next = (i, j+1)
                if all([p not in current_pos for p in to_check]):
                    p = prop_next
                    break
        if p is not None:
            prop[p] = prop.get(p,[]) + [elf]
    return prop

def move_elves(elves: dict, proposed: dict) -> tuple:
    n = 0
    for pos, to_move in proposed.items():
        if len(to_move) == 1:
            elves[to_move[0]] = pos
            n += 1
    return elves, n

def disperse_elves(elves: dict, rounds: int = inf) -> tuple:
    dirs = ['N', 'S', 'W', 'E']
    moved = inf
    r = 0
    while moved > 0 and r <= rounds:
        proposed = compute_proposed_positions(elves, dirs)
        dirs = dirs[1:] + [dirs[0]]
        elves, moved = move_elves(elves, proposed)
        r += 1
    return elves, r

def count_empty_tiles(elves: dict):
    rows = [i for i,_ in elves.values()]
    cols = [j for _,j in elves.values()]
    return (max(rows)-min(rows)+1) * (max(cols)-min(cols)+1) - len(elves)


if __name__ == '__main__':
    input = read_file_into_list(path='23_Unstable_Diffusion/23_input.txt')
    elves_input = process_elves(input)

    elves, _ = disperse_elves(elves_input.copy(), rounds=10)
    answer = count_empty_tiles(elves)
    print(f'Answer to part 1: {answer}')

    _, rounds = disperse_elves(elves_input.copy())
    answer = rounds
    print(f'Answer to part 2: {answer}')
