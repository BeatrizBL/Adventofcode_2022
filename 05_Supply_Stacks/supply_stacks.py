from helpers import read_file_into_list
import re

def _format_input_stacks(input_stacks: list) -> list:
    input_stacks = [[s[i:(i+3)] for i in range(0, len(s), 4)] for s in input_stacks]
    input_stacks = [[s.strip().replace('[', '').replace(']','') for s in l] for l in input_stacks]
    return input_stacks

def process_input_stacks(input_stacks: list) -> list:
    n_stacks = max([int(n) for n in input_stacks.pop().strip().split(' ') if len(n)>0])
    input_stacks = _format_input_stacks(input_stacks)
    input_stacks.reverse()
    stacks = [[] for _ in range(n_stacks)]
    for level in input_stacks:
        for i, crate in enumerate(level):
            if len(crate) > 0:
                stacks[i].append(crate)
    return stacks

def _format_movement(movement: str) -> dict:
    return {
        'quantity': int(re.search('move (\d+?) from \d+ to \d+', movement).group(1)),
        'from': int(re.search('move \d+ from (\d+?) to \d+', movement).group(1))-1,
        'to': int(re.search('move \d+ from \d+ to (\d+?)', movement).group(1))-1
    }

def process_input_movements(movements: list) -> list:
    return [_format_movement(m) for m in movements]

def move_crates_single(stacks: list, movements: list) -> list:
    moved_stacks = [l.copy() for l in stacks]
    for m in movements:
        for i in range(m['quantity']):
            if len(moved_stacks[m['from']]) == 0:
                raise IndexError(f'No crate to move in stack {i+1}')
            moved_stacks[m['to']].append(moved_stacks[m['from']].pop())
    return moved_stacks

def move_crates_multiple(stacks: list, movements: list) -> list:
    moved_stacks = [l.copy() for l in stacks]
    for m in movements:
        to_move = []
        for i in range(m['quantity']):
            if len(moved_stacks[m['from']]) == 0:
                raise IndexError(f'No crate to move in stack {i+1}')
            to_move.append(moved_stacks[m['from']].pop())
        to_move.reverse()
        moved_stacks[m['to']].extend(to_move)
    return moved_stacks

def check_top_crates(stacks: list) -> list:
    top_crates = []
    for stack in stacks:
        top_crates.append(stack[-1] if len(stack) > 0 else ' ')
    return top_crates


if __name__ == '__main__':
    input_stacks, input_movements = read_file_into_list(
        path='05_Supply_Stacks/5_input.txt',
        split_list_char='\n',
        drop_spaces=False
    )
    stacks = process_input_stacks(input_stacks=input_stacks)
    movements = process_input_movements(input_movements)

    final_stacks = move_crates_single(stacks=stacks, movements=movements)
    answer = ''.join(check_top_crates(stacks=final_stacks))
    print(f'Answer to part 1: {answer}')

    final_stacks = move_crates_multiple(stacks=stacks, movements=movements)
    answer = ''.join(check_top_crates(stacks=final_stacks))
    print(f'Answer to part 2: {answer}')
