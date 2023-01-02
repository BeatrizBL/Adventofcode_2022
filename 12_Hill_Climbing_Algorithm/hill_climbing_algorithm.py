from helpers import read_file_into_list
from graph import Graph

def _create_positions(g: Graph, input: list) -> tuple:
    start = None
    end = None
    for i, line in enumerate(input):
        for j, s in enumerate(line):
            position = (i,j)
            if s == 'S':
                start = position
                height = 'a'
            elif s == 'E':
                end = position
                height = 'z'
            else:
                height = s
            height = ord(height) - ord('a')
            g.add_update_node(node=position, value=height)
    return start, end

def _link_positions(g: Graph, n: int, m: int):
    for i in range(n):
        for j in range(m):
            h = g.get_node((i,j))
            neigh = [((i-1,j), g.get_node((i-1,j), ignore_errors=True)), # Up
                     ((i+1,j), g.get_node((i+1,j), ignore_errors=True)), # Down
                     ((i,j-1), g.get_node((i,j-1), ignore_errors=True)), # Left
                     ((i,j+1), g.get_node((i,j+1), ignore_errors=True))] # Right
            for pn, hn in neigh:
                if hn is not None and (h+1) >= hn:
                    g.add_edge((i,j), pn)

def process_map_graph(input: list) -> tuple:
    g = Graph(directed=True)
    start, end = _create_positions(g, input)
    _link_positions(g, n=len(input), m=len(input[0]))
    return g, start, end

def find_general_shortest_path(
    g: Graph, 
    end: tuple,
    starting_height: int = 0
) -> list:
    starts = [n for n,v in g.get_nodes().items() if v==starting_height]
    min_path = None
    for s in starts:
        path = g.find_shortest_path_BFS(s, end)
        if min_path is None or ( path is not None and len(path) < len(min_path) ):
            min_path = path
    return min_path


if __name__ == '__main__':
    input = read_file_into_list(path='12_Hill_Climbing_Algorithm/12_input.txt')
    height_map, start, end = process_map_graph(input)
    answer = len(height_map.find_shortest_path_BFS(start,end)) - 1
    print(f'Answer to part 1: {answer}')

    answer = len(find_general_shortest_path(height_map, end)) - 1
    print(f'Answer to part 2: {answer}')
