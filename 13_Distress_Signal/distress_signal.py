from helpers import read_file_into_list
import re
import copy


def find_next_number(s: str) -> int:
    search = re.search('(\d+?)[,\]*]', s)
    if search is None:
        if s.isdigit():
            return int(s)
        else:
            raise ValueError(f'Unknown number format for {s}')
    return int(search.group(1))

def string_to_list(s: str, i: int = 0) -> tuple:
    l = []
    while i < len(s):
        if s[i] == '[':
            res, j = string_to_list(s, i+1)
            l.append(res)
            i = j
        elif s[i] == ']':
            return l, i+1
        elif s[i] != ',':
            n = find_next_number(s[i:])
            l.append(n)
            i += len(str(n))
        else:
            i += 1
    return l, len(s)

def process_lists(input: list) -> list:
    l = []
    for left, right in input:
        list_left, _ = string_to_list(left)
        list_right, _ = string_to_list(right)
        l.append([list_left[0], list_right[0]])
    return l

def _check_right_order(left: list, right: list) -> bool:
    if len(left) == 0 and len(right) > 0:
        return True
    if len(left) > 0 and len(right) == 0:
        return False
    if len(left) == 0 and len(right) == 0:
        return None
    l = left.pop(0)
    r = right.pop(0)
    if isinstance(l, int) and isinstance(r, int):
        res = ( l < r ) if l != r else None
    elif isinstance(l, list) and isinstance(r, list):
        res = check_right_order(l, r)
    elif isinstance(l, int) and isinstance(r, list):
        res = check_right_order([l], r)
    elif isinstance(l, list) and isinstance(r, int):
        res = check_right_order(l, [r])
    else:
        raise ValueError('Unknown types for inputs')
    if res is None:
        res = check_right_order(left, right)
    return res

def check_right_order(left: list, right: list) -> bool:
    return _check_right_order(copy.deepcopy(left), copy.deepcopy(right))

def check_pair_order(pairs: list):
    return [check_right_order(l,r) for l,r in pairs]

def bubble_sort(packets: list):
    n = len(packets)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if check_right_order(packets[j], packets[j+1]) is False:
                swapped = True
                packets[j], packets[j+1] = packets[j+1], packets[j]
        if not swapped:
            return


if __name__ == '__main__':
    input = read_file_into_list(
        path='13_Distress_Signal/13_input.txt',
        split_list_char='\n'
    )
    pairs = process_lists(input)
    orders = check_pair_order(pairs)
    answer = sum([i+1 for i,v in enumerate(orders) if v])
    print(f'Answer to part 1: {answer}')

    pairs = process_lists(input)
    packets = [l for pair in pairs for l in pair] + [[[2]], [[6]]]
    bubble_sort(packets)
    answer = ( packets.index([[2]]) + 1 ) * ( packets.index([[6]]) + 1 )
    print(f'Answer to part 2: {answer}')

