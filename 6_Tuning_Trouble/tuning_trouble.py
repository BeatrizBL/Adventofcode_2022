from helpers import read_file_into_list
from itertools import islice

def find_package_start(
    datastream: str,
    marker_size: int = 4
) -> int:
    for i in range(len(datastream) - marker_size + 1):
        if len(set(datastream[i:(i+marker_size)])) == marker_size:
            return i + marker_size
    return None


if __name__ == '__main__':
    datastream = read_file_into_list(path='6_Tuning_Trouble/6_input.txt')[0]
    answer = find_package_start(datastream=datastream)
    print(f'Answer to part 1: {answer}')

    answer = find_package_start(datastream=datastream, marker_size=14)
    print(f'Answer to part 2: {answer}')
