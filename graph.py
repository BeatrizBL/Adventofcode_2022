class Graph:

    def __init__(self, directed: bool = True):
        self._graph_dict = {}
        self._nodes = {}
        self.directed = directed

    def add_update_node(self, node, value = None):
        self._nodes[node] = value
        if node not in self._graph_dict:
            self._graph_dict[node] = []

    def add_edge(self, node, neighbor):
        if node not in self._graph_dict:
            self._graph_dict[node] = [neighbor]
        elif neighbor not in self._graph_dict[node]:
            self._graph_dict[node].append(neighbor)
        
        if neighbor not in self._graph_dict:
            self._graph_dict[neighbor] = []
        
        if node not in self._nodes:
            self._nodes[node] = None
        if neighbor not in self._nodes:
            self._nodes[neighbor] = None

        # Add edge back for non-directed graphs
        if not self.directed and node not in self._graph_dict[neighbor]:
            self._graph_dict[neighbor].append(node)

    def get_nodes(self):
        return self._nodes

    def get_node(self, node, ignore_errors: bool = False):
        if node not in self.get_nodes() and not ignore_errors:
            raise ValueError(f'Node {node} not available in the graph!')
        return self._nodes.get(node, None)

    def get_neighbors(self, node):
        if node not in self.get_nodes():
            raise ValueError(f'Node {node} not available in the graph!')
        return self._graph_dict[node]

    def print_edges(self):
        for node in self._graph_dict:
            for neighbor in self._graph_dict[node]:
                print('(', node, ', ', neighbor, ')')

    def find_path_DFS(self, start, end) -> list:
        for node in [start, end]:
            if node not in self.get_nodes():
                raise ValueError(f'Node {node} not available in the graph!')

        stack = [(start, [start])]
        while stack:
            (node, path) = stack.pop()
            for next in set(self.get_neighbors(node)) - set(path):
                if next == end:
                    return path + [next]
                else:
                    stack.append((next, path + [next]))

    def find_shortest_path_BFS(self, start, end) -> list:
        for node in [start, end]:
            if node not in self.get_nodes():
                raise ValueError(f'Node {node} not available in the graph!')
        
        queue = [(start, [])]
        visited = [start]
        while len(queue) > 0:
            node, path = queue.pop(0)
            if node == end:
                return path + [end]
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, path+[node]))
                    visited.append(neighbor)


class Tree(Graph):

    def __init__(self):
        super().__init__(directed=True)
        self._parent_nodes = {}

    def add_edge(self, node, neighbor):
        if neighbor in self._parent_nodes:
            raise ValueError(f'Node {neighbor} already part of the tree structure!')
        super().add_edge(node, neighbor)
        self._parent_nodes[neighbor] = node

    def get_parent_node(self, node):
        if node not in self._nodes:
            raise ValueError(f'Node {node} not available in the graph!')
        return self._parent_nodes.get(node, None)

    def get_child_nodes(self, node):
        return self.get_neighbors(node)


def compute_graph_distances(g: Graph, nodes: list = None) -> dict:
    dist = {}
    nodes = g.get_nodes().keys() if nodes is None else nodes
    for start in nodes:
        for end in nodes:
            if start != end and (start,end) not in dist:
                d = len(g.find_shortest_path_BFS(start, end)) - 1
                dist[(start,end)] = d
                if not g.directed:
                    dist[(end,start)] = d
    return dist
