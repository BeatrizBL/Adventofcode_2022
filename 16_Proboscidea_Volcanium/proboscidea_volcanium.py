import sys
sys.path.append('/home/usuario/Desktop/Personal/Adventofcode_2022')

from helpers import read_file_into_list
from graph import Graph
import re

def build_valve_graph(input: list) -> Graph:
    g = Graph(directed=False)
    for line in input:
        valve = re.search('Valve ([A-Z]{2}?)', line).group(1)
        flow_rate = int(re.search('has flow rate=(\d+?);', line).group(1))
        g.add_update_node(node=valve, value=flow_rate)
        for neigh in re.search('lead[s]{0,1} to valve[s]{0,1} (.+?)$', line).group(1).split(','):
            g.add_edge(valve, neighbor=neigh.strip())
    return g

def find_possible_paths(
    tunnels: Graph,
    start_valve: str,
    max_steps: int,
    valve_step: int = 1,
    move_step: int = 1
) -> list:
    if start_valve not in tunnels.get_nodes():
        raise ValueError(f'Node {start_valve} not available in the graph!')
    n_valves = len([v for v,p in tunnels.get_nodes().items() if p>0])
    final_opens = []
    queue = [(start_valve, 0, [])]
    while len(queue) > 0:
        valve, steps, open_valves = queue.pop(0)
        if steps >= max_steps or len(open_valves) == n_valves:
            if len(open_valves) > 0 and open_valves not in final_opens:
                final_opens.append(open_valves) # Nothing possible
        else:
            if ( steps + valve_step ) <= max_steps and ( steps + move_step + valve_step ) > max_steps:
                if valve not in [v for v,_ in open_valves] \
                    and tunnels.get_node(valve) > 0 \
                    and (open_valves + [(valve, steps + valve_step)]) not in final_opens:
                    final_opens.append(open_valves + [(valve, steps + valve_step)]) # Just open the current valve
            else:
                neighbors = tunnels.get_neighbors(valve)
                if ( steps + move_step ) <= max_steps:
                    queue.extend([(neigh, steps + move_step, open_valves) for neigh in neighbors]) # Move without opening
                if steps + move_step + valve_step <= max_steps:
                    if valve not in [v for v,_ in open_valves] and tunnels.get_node(valve) > 0: # Open and move
                        queue.extend([(neigh, steps + move_step + valve_step, open_valves + [(valve, steps + valve_step)]) for neigh in neighbors])
    return final_opens

def compute_pressure(
    tunnels: Graph,
    path: list,
    max_steps: int
) -> int:
    return sum([tunnels.get_node(v) * (max_steps-t) for v,t in path])

def compute_max_pressure(
    tunnels: Graph,
    start_valve: str,
    max_steps: int,
    valve_step: int = 1,
    move_step: int = 1
) -> int:
    paths = find_possible_paths(tunnels, start_valve, max_steps, valve_step, move_step)
    return max([compute_pressure(tunnels, p, max_steps) for p in paths])


if __name__ == '__main__':
    input = read_file_into_list(path='16_Proboscidea_Volcanium/16_example.txt')
    tunnels = build_valve_graph(input)
    answer = compute_max_pressure(tunnels, start_valve='AA', max_steps=30)
    print(f'Answer to part 1: {answer}')

    answer = None
    print(f'Answer to part 2: {answer}')
