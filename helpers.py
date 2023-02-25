from math import gcd


def clean_string_list(
    l: str,
    drop_spaces: bool = True
) -> list:
    def _clean_string(s: str) -> str:
        s = s.strip() if drop_spaces else s.replace('\n', '')
        return (s if len(s)>0 else None)
    l = [(_clean_string(s) if not isinstance(s, list) else clean_string_list(s, drop_spaces=drop_spaces)) for s in l] 
    l = [s for s in l if s is not None] 
    return l if len(l)>0 else None

def read_file_into_list(
    path: str,
    split_list_char: str = None,
    drop_spaces: bool = True
) -> list:
    with open(path) as f:
        lines = f.readlines()
    if split_list_char is not None:
        cuts = [i for i, x in enumerate(lines) if x == split_list_char]
        cuts = [0] + cuts + [len(lines)]
        lines = [[s for s in lines[i:j]] for i,j in zip(cuts[:(len(cuts)-1)], cuts[1:len(cuts)])]
    return clean_string_list(lines, drop_spaces=drop_spaces)


def print_sparse_matrix(
    matrix: dict, 
    empty_char: str = '.'
):
    """Prints an sparse matrix defined as a dictionary, where the keys are tuples of (i,j)
    positions in the matrix.

    Args:
        matrix (dict): Matrix to print.
        empty_char (str, optional): Character to be used for positions that are not available
            in the dictionary. Defaults to '.'.
    """
    y1 = min([i for i,_ in list(matrix.keys())])
    y2 = max([i for i,_ in list(matrix.keys())])
    x1 = min([j for _,j in list(matrix.keys())])
    x2 = max([j for _,j in list(matrix.keys())])
    for i in range(y1, y2+1):
        line = ''
        for j in range(x1, x2+1):
            line += str(matrix.get((i,j), empty_char))
        print(line)


def compute_least_common_multiple(values: list) -> int:
    lcm = 1
    for i in range(len(values)):
        lcm = int( lcm * values[i] / gcd(lcm, values[i]) )
    return lcm


def manhattan_distance(p: tuple, q: tuple) -> int:
    return abs(p[0]-q[0]) + abs(p[1]-q[1])


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
