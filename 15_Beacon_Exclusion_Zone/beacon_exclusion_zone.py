from helpers import read_file_into_list, manhattan_distance
import re

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

def _combine_patches(patches: list) -> list:
    covered = []
    patches = sorted(patches, key=lambda x: x[0])
    interval_start, interval_end = patches[0]
    for start, end in patches[1:]:
        if start > interval_end:
            covered.append((interval_start, interval_end))
            interval_start = start
            interval_end = end
        elif interval_end < end:
            interval_end = end
    covered.append((interval_start, interval_end))
    return covered      

def covered_positions_in_row(
    sensors: list, 
    row: int,
    limits: tuple = None
) -> list:
    patches = []
    for s in sensors:
        x,y = s[0]
        d = manhattan_distance((x,y), (x,row))
        if d <= s[2]:
            to_cover = abs(s[2] - d)
            new_start = x-to_cover
            new_end = x+to_cover
            if limits is not None:
                new_start = min(max(new_start, limits[0]), limits[1])
                new_end = min(max(new_end, limits[0]), limits[1])
            patches.append((new_start, new_end))
    covered = _combine_patches(patches)
    return covered

def count_not_beacon_positions_in_row(sensors: list, row: int) -> int:
    covered = covered_positions_in_row(sensors, row=row)
    covered_length = sum([(e-s+1) for s,e in covered])
    return covered_length - len(set([b for _,b,_ in sensors if b[1]==row]))

def find_distress_beacon(
    sensors: list, 
    limits: tuple, 
    verbose: bool = False
) -> tuple:
    domain = set(range(limits[0], limits[1]+1))
    for row in domain:
        if verbose and row % 100000 == 0 and row > 0:
            print(f'{row} / {limits[1]}')
        covered = covered_positions_in_row(sensors, row=row, limits=limits)
        covered_length = sum([(e-s+1) for s,e in covered])
        if covered_length < len(domain):
            covered_sets = [set(range(s,e+1)) for s,e in covered]
            return ( list(domain - set().union(*covered_sets))[0], row )


if __name__ == '__main__':
    input = read_file_into_list(path='15_Beacon_Exclusion_Zone/15_input.txt')
    sensors = process_input(input)
    
    answer = count_not_beacon_positions_in_row(sensors, row=2000000)
    # answer = count_not_beacon_positions_in_row(sensors, row=10) # Example
    print(f'Answer to part 1: {answer}')

    distress_beacon = find_distress_beacon(
        sensors, 
        limits=(0,4000000), 
        verbose=True
    )
    # distress_beacon = find_distress_beacon(sensors, limits=(0,20)) # Example
    answer = ( distress_beacon[0] * 4000000 + distress_beacon[1] ) if distress_beacon is not None else None
    print(f'Answer to part 2: {answer}')
