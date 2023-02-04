from helpers import read_file_into_list
from math import sqrt

def input_to_vectors(input: list) -> list:
    return [[int(c) for c in s.split(',')] for s in input]


class Droplet():

    def __init__(
        self, 
        positions: list
    ):
        self.cubes = {tuple(p): i for i,p in enumerate(positions)}
        self._distance_matrix = None
        self._casing = self._find_limits()

    @property
    def distance_matrix(self) -> list:
        if self._distance_matrix is None:
            self._distance_matrix = self.build_distance_matrix()
        return self._distance_matrix

    def build_distance_matrix(self) -> list:
        dist = [[None]*len(self.cubes) for _ in range(len(self.cubes))]
        for p, i in self.cubes.items():
            for q, j in self.cubes.items():
                if i > j:
                    d = sqrt( (p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2 )
                    dist[i][j] = d
                    dist[j][i] = d
        return dist

    def count_surface(self) -> int:
        surface = 0
        for id in self.cubes.values():
            surface += (6 - sum([1 for d in self.distance_matrix[id] if d==1]))
        return surface

    def _find_limits(self) -> list:
        limits = []
        for d in [0,1,2]:
            values = [p[d] for p in self.cubes.keys()]
            limits.append([min(values)-1, max(values)+1])
        return limits

    def _within_casing_limits(self, p: tuple) -> bool:
            for i, limits in enumerate(self._casing):
                if p[i] < limits[0] or p[i] > limits[1]:
                    return False
            return True

    def count_external_sides(self) -> int:
        start = (self._casing[0][0], self._casing[1][0], self._casing[2][0])
        visited = []
        to_visit = [start]
        sides = 0
        adj_moves = [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]
        while len(to_visit) > 0:
            pos = to_visit.pop(0)
            adj = [(pos[0]+m[0], pos[1]+m[1], pos[2]+m[2]) for m in adj_moves] 
            sides += sum([1 for p in adj if p in self.cubes])
            to_visit.extend([p for p in adj if self._within_casing_limits(p) and \
                                               p not in self.cubes and \
                                               p not in visited and \
                                               p not in to_visit])
            visited.append(pos)
        return sides


if __name__ == '__main__':
    input = read_file_into_list(path='18_Boiling_Boulders/18_input.txt')
    cubes = input_to_vectors(input)

    droplet = Droplet(cubes)
    answer = droplet.count_surface()
    print(f'Answer to part 1: {answer}')

    answer = droplet.count_external_sides()
    print(f'Answer to part 2: {answer}')
