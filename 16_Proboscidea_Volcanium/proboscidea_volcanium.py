import sys
sys.path.append('/home/usuario/Desktop/Personal/Adventofcode_2022')

from helpers import read_file_into_list
from graph import Graph, compute_graph_distances
import re
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    @property
    def empty(self) -> bool:
        return len(self.elements) == 0
    
    def add(self, item, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.elements)[1]


def build_valve_graph(input: list) -> Graph:
    g = Graph(directed=False)
    for line in input:
        valve = re.search('Valve ([A-Z]{2}?)', line).group(1)
        flow_rate = int(re.search('has flow rate=(\d+?);', line).group(1))
        g.add_update_node(node=valve, value=flow_rate)
        for neigh in re.search('lead[s]{0,1} to valve[s]{0,1} (.+?)$', line).group(1).split(','):
            g.add_edge(valve, neighbor=neigh.strip())
    return g

def heuristic(
    valve: str,
    remaining_steps: int,
    closed_valves: list,
    distances: dict
) -> int:
    final_steps = {v: (remaining_steps - distances[(valve, v)] - 1) for v in closed_valves}
    return sum([ max(0, final_steps[v]) * tunnels.get_node(v) for v in closed_valves])

def compute_max_pressure(
    tunnels: Graph,
    start_valve: str,
    max_steps: int
) -> int:
    valves = {v: -1 for v,p in tunnels.get_nodes().items() if p>0}
    dist = compute_graph_distances(
        g=tunnels, 
        nodes=[start_valve]+list(valves.keys())
    )
    queue = PriorityQueue()
    queue.add((start_valve, max_steps, valves.copy(), 0), 0)
    iter = 0
    while not queue.empty:
        valve, remaining_steps, to_open, gain = queue.pop()
        next_valves = [v for v, n in to_open.items() if n==-1 and ( dist[valve, v] + 1 ) <= remaining_steps]
        if remaining_steps <= 0 or len(next_valves) == 0:
            break
        for next_valve in next_valves:
            iter += 1 # To break ties in priority by picking the first added one
            steps = dist[valve, next_valve] + 1
            new_gain = gain + (remaining_steps - steps) * tunnels.get_node(next_valve)
            next_to_open = to_open.copy()
            next_to_open[next_valve] = max( max(to_open.values()) + 1, 1)
            h = heuristic(
                valve=next_valve, 
                remaining_steps=(remaining_steps - steps), 
                closed_valves=[v for v, n in next_to_open.items() if n==-1], 
                distances=dist
            )
            priority = new_gain + h
            queue.add((next_valve, (remaining_steps - steps), next_to_open, new_gain), (1 / priority, iter))
    return gain


if __name__ == '__main__':
    input = read_file_into_list(path='16_Proboscidea_Volcanium/16_input.txt')
    tunnels = build_valve_graph(input)
    answer = compute_max_pressure(tunnels, start_valve='AA', max_steps=30)
    print(f'Answer to part 1: {answer}')

    answer = None
    print(f'Answer to part 2: {answer}')
