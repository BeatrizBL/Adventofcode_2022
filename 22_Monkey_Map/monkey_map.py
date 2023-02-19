import sys
sys.path.append('/home/usuario/Desktop/Personal/Adventofcode_2022')

from helpers import read_file_into_list

def process_board(board_str: list) -> dict:
    board = {}
    for i, s in enumerate(board_str):
        for j, c in enumerate(s):
            if c != ' ':
                board[(i+1, j+1)] = c
    return board

def process_path(
    path_str: str,
    start_dir_idx: int = 0,
    directions: list = ['>', 'v', '<', '^']
) -> list:
    idx = [0] + [i for i, c in enumerate(path_str) if c in ['L', 'R']] + [len(path_str)]
    slices = [path_str[s:e] for s,e in list(zip(idx[:-1], idx[1:]))]
    path = []
    for i, s in enumerate(slices):
        if i==0:
            dir_idx = start_dir_idx
            n = int(s)
        else:
            dir_idx = (dir_idx + 1) % len(directions) if s[0] == 'R' else (dir_idx - 1) % len(directions)
            n = int(s[1:])
        path.append((directions[dir_idx], n))
    return path

def define_start(board: dict) -> tuple:
    top_cols = [j for i,j in board.keys() if i==1]
    return (1, min(top_cols))

def process_direction(position: tuple, direction: str) -> tuple:
    i, j = position
    if direction == '^':
        return (i-1, j)
    if direction == '>':
        return (i, j+1)
    if direction == 'v':
        return (i+1, j)
    if direction == '<':
        return (i, j-1)

def wrap_board(board: dict, position: tuple, direction: str) -> tuple:
    i, j = position
    if direction in ['^', 'v']:
        rows = [x for x,y in board.keys() if y==j]
        return (min(rows) if direction=='v' else max(rows), j)
    if direction in ['>', '<']:
        cols = [y for x,y in board.keys() if x==i]
        return (i, min(cols) if direction=='>' else max(cols))

def follow_path(
    board: dict,
    path: list,
    start: tuple = None,
    rock_symbol: str = '#'
) -> tuple:
    i, j = start if start is not None else define_start(board)
    for d, n in path:
        for _ in range(n):
            ni, nj = process_direction((i,j), d)
            if (ni,nj) not in board:
                ni,nj = wrap_board(board, (ni,nj), d)
            if board[(ni,nj)] != rock_symbol:
                i,j = ni,nj
            else:
                break
    return (i,j), d

def compute_password(
    board: dict,
    path: list,
    row_score: int = 1000,
    col_score: int = 4,
    dir_scores: dict = {'>': 0, 'v': 1, '<': 2, '^': 3}
) -> int:
    (row, col), dir = follow_path(board, path)
    return row_score * row + col_score * col + dir_scores[dir]


if __name__ == '__main__':
    input_board, input_path = read_file_into_list(
        path='22_Monkey_Map/22_input.txt', 
        drop_spaces=False,
        split_list_char='\n'
    )
    board = process_board(input_board)
    path = process_path(input_path[0])

    answer = compute_password(board, path)
    print(f'Answer to part 1: {answer}')

    answer = None
    print(f'Answer to part 2: {answer}')
