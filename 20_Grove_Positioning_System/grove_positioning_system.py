from helpers import read_file_into_list

def get_value_ids(input: list) -> dict:
    return {i: int(v) for i,v in enumerate(input)}

def mix_numbers_iter(
    values: dict, 
    pos: list = None,
    verbose: bool = False
) -> list:
    n = len(values)
    pos = list(range(n)) if pos == None else pos
    for id in range(n):
        p = pos.index(id)
        v = values[id]
        v = (v % (n-1)) if v >= 0 else - ((-v) % (n-1))
        newp = ( p + v ) % n
        pos.remove(id)
        if v < 0 and newp > p: # Overflows on the left
            pos.insert(newp - 1, id)
        elif v > 0 and newp < p: # Overflows on the right
            pos.insert(newp + 1, id)
        else:
            pos.insert(newp, id)
        if verbose:
            print([values[i] for i in pos])
    return pos

def mix_numbers(
    values: dict, 
    key: int = 1,
    n_iters: int = 1,
    verbose: bool = False
) -> list:
    adj_values = values.copy()
    adj_values = {id: v * key for id,v in adj_values.items()}
    pos = None
    for _ in range(n_iters):
        pos = mix_numbers_iter(values=adj_values, pos=pos, verbose=verbose)
    return [adj_values[i] for i in pos]

def compute_grove_coordinates(
    mixed: list,
    positions: list,
    reference: int = 0
) -> int:
    n = len(mixed)
    start = mixed.index(reference)
    res = 0
    for p in positions:
        res += mixed[(start+p)%n]
    return res


if __name__ == '__main__':
    input = read_file_into_list(path='20_Grove_Positioning_System/20_input.txt')
    values = get_value_ids(input)

    mixed = mix_numbers(values)
    answer = compute_grove_coordinates(mixed, [1000, 2000, 3000])
    print(f'Answer to part 1: {answer}')

    mixed = mix_numbers(values, key=811589153, n_iters=10)
    answer = compute_grove_coordinates(mixed, [1000, 2000, 3000])
    print(f'Answer to part 2: {answer}')
