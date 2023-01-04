from helpers import read_file_into_list
import re

def manhattan_distance(p: tuple, q: tuple) -> int:
    return abs(p[0]-q[0]) + abs(p[1]-q[1])

def break_down_line(line: str) -> tuple:
    """For a line with format:
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15'
    Returns a tuple of three elements,
    - Sensor coordinates - (2, 18)
    - Beacon coordinates - (-2, 15)
    - Manhattan distance between both - 7
    """
    sensor_x = int(re.search('Sensor at x=((-{0,1}\d+)?), y', line).group(1))
    sensor_y = int(re.search('y=((-{0,1}\d+)?):', line).group(1))
    beacon_x = int(re.search('closest beacon is at x=((-{0,1}\d+)?),', line).group(1))
    beacon_y = int(re.search('closest beacon is at x=-{0,1}\d+, y=((-{0,1}\d+)?)', line).group(1))
    return (
        (sensor_x, sensor_y),
        (beacon_x, beacon_y),
        manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))
    )

def process_input(input: list) -> list:
    sensors = []
    for line in input:
        sensors.append(break_down_line(line))
    return sensors

def covered_positions_in_row(
    sensors: list, 
    row: int,
    domain: set = None
) -> set:
    covered = set()
    for s in sensors:
        x,y = s[0]
        d = manhattan_distance((x,y), (x,row))
        if d <= s[2]:
            to_cover = abs(s[2] - d)
            new = set(range(x-to_cover, x+to_cover+1))
            if domain is not None:
                new = new.intersection(domain)
            covered = covered.union(new)
    return covered

def count_not_beacon_positions_in_row(sensors: list, row: int) -> int:
    covered = covered_positions_in_row(sensors, row=row)
    return len(covered) - len(set([b for _,b,_ in sensors if b[1]==row]))

def find_distress_beacon(sensors: list, limits: tuple) -> tuple:
    domain = set(range(limits[0], limits[1]+1))
    for row in domain:
        covered = covered_positions_in_row(sensors, row=row, domain=domain)
        if len(covered) < len(domain):
            return ( list(domain - covered)[0], row )


if __name__ == '__main__':
    input = read_file_into_list(path='15_Beacon_Exclusion_Zone/15_example.txt')
    sensors = process_input(input)
    
    # answer = count_not_beacon_positions_in_row(sensors, row=2000000)
    answer = count_not_beacon_positions_in_row(sensors, row=10)
    print(f'Answer to part 1: {answer}')

    # distress_beacon = find_distress_beacon(sensors, limits=(0,4000000))
    distress_beacon = find_distress_beacon(sensors, limits=(0,20))
    answer = distress_beacon[0] * 4000000 + distress_beacon[1]
    print(f'Answer to part 2: {answer}')
