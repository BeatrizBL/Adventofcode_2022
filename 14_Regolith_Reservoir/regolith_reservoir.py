from helpers import read_file_into_list, print_sparse_matrix

def process_input_points(input: list) -> list:
    points = [s.split(' -> ') for s in input]
    points = [[s.split(',') for s in l] for l in points]
    points = [[(int(x), int(y)) for x,y in l] for l in points]
    return points

def connect_points(points: list, pouring_point: tuple = (500,0)) -> dict:
    slice = {}
    for l in points:
        for (x1,y1), (x2,y2) in zip(l[:(len(l)-1)], l[1:]):
            for x in range(min(x1,x2), max(x1,x2)+1):
                for y in range(min(y1,y2), max(y1,y2)+1):
                    slice[(y,x)] = '#'  # Transposed to (i,j) matrix notation
    slice[(pouring_point[1]), (pouring_point[0])] = '+'
    return slice

def pour_sand_unit(
    slice: dict,
    start_symbol: str = '+',
    blocker_symbols: list = ['#', 'o']
) -> tuple:
    bottom = max([i for i,j in slice.keys()])
    pos = list(slice.keys())[list(slice.values()).index(start_symbol)]
    moving = True
    while moving:
        i,j = pos
        if i == bottom:
            moving = None
            pos = None
        else:
            mov = [(p, slice.get(p,None)) for p in [(i+1,j), (i+1,j-1), (i+1,j+1)]]
            next_pos = [p for p,v in mov if v not in blocker_symbols]
            if len(next_pos) == 0:
                moving = False
            else:
                pos = next_pos[0]
    return pos

def pour_sand(
    slice: dict,
    sand_symbol: str = 'o',
    start_symbol: str = '+',
    rock_symbol: str = '#',
    verbose: int = 0
) -> tuple:
    start = list(slice.keys())[list(slice.values()).index(start_symbol)]
    n = 0
    stop_pouring = False
    while not stop_pouring:
        sand_pos = pour_sand_unit(
            slice, 
            start_symbol=start_symbol,
            blocker_symbols=[sand_symbol, rock_symbol]
        )
        if sand_pos is None:
            stop_pouring = True
        else:
            n += 1
            slice[sand_pos] = sand_symbol
            if verbose == 2:
                print_sparse_matrix(slice)
            if sand_pos == start:
                stop_pouring = True
    if verbose >= 1:
        print_sparse_matrix(slice)
    return slice, n

def add_floor(
    slice: dict,
    floor_distance: int = 2,
    start_symbol: str = '+',
    floor_symbol: str = '#'
) -> dict:
    bottom = max([i for i,j in slice.keys()])
    start = list(slice.keys())[list(slice.values()).index(start_symbol)]
    max_distance = (bottom - start[0]) + floor_distance
    for j in range(start[1]-max_distance, start[1]+max_distance+1):
        slice[(bottom+floor_distance, j)] = floor_symbol
    return slice


if __name__ == '__main__':
    input = read_file_into_list(path='14_Regolith_Reservoir/14_input.txt')
    points = process_input_points(input)
    rock_slice = connect_points(points)

    rock_slice, answer = pour_sand(rock_slice, verbose=1)
    print(f'Answer to part 1: {answer}')

    rock_slice = connect_points(points)
    rock_slice = add_floor(rock_slice)
    rock_slice, answer = pour_sand(rock_slice, verbose=0)
    print(f'Answer to part 2: {answer}')
