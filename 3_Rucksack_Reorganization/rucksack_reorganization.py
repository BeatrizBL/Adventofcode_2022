from functools import reduce
from helpers import read_file_into_list

def split_compartments(rucksacks: list) -> list:
    return [[l[:int(len(l)/2)], l[int(len(l)/2):]] for l in rucksacks]

def find_common_items(item_lists: list) -> list:
    return [list(set.intersection(*[set(s) for s in items])) for items in item_lists]

def compute_priorities(errors: list) -> list:
    def _symbol_priority(s: str) -> int:
        if 'a' <= s and s <= 'z':
            return ord(s) - ord('a') + 1
        if 'A' <= s and s <= 'Z':
            return ord(s) - ord('A') + 27
    return [[_symbol_priority(s) for s in l] for l in errors]

def compute_total_priority(priorities: list) -> int:
    return sum([sum(l) for l in priorities])

def split_elf_groups(
    rucksacks: list,
    n_elves: int = 3
) -> list:
    return [rucksacks[i:(i+3)] for i in range(0, len(rucksacks), n_elves)]


if __name__ == '__main__':
    rucksacks = read_file_into_list(path='3_Rucksack_Reorganization/3_input.txt')
    answer = reduce(
        lambda v, f: f(v), 
        (split_compartments,
         find_common_items,
         compute_priorities,
         compute_total_priority), 
        rucksacks
    )
    print(f'Answer to part 1: {answer}')

    answer = reduce(
        lambda v, f: f(v), 
        (split_elf_groups,
         find_common_items,
         compute_priorities,
         compute_total_priority), 
        rucksacks
    )
    print(f'Answer to part 2: {answer}')
