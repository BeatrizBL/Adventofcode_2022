from helpers import read_file_into_list

def interval_to_binary(s: str) -> int:
    start, end = (int(v) for v in s.split('-'))
    b = '1'*(end-start+1) + '0'*(start-1)
    return int(b, base=2)

def format_input_sections(sections: list) -> list:
    """Formats input list like ['2-4,6-8', '2-3,4-5'] to a list of lists.
    The elements of each sublist are the binary representation of each
    interval. For instance, 2-4 would be 0000001110 (i.e. 14).
    """
    return [[interval_to_binary(i) for i in s.split(',')] for s in sections]

def count_full_intersections(binary_sections: list) -> int:
    common = [(s1 & s2) == min(s1,s2) for s1, s2 in binary_sections]
    return sum(common)

def count_some_intersection(binary_sections: list) -> int:
    some = [(s1 & s2) != 0 for s1, s2 in binary_sections]
    return sum(some)


if __name__ == '__main__':
    sections = read_file_into_list(path='4_Camp_Cleanup/4_input.txt')
    binary_sections = format_input_sections(sections)
    
    answer = count_full_intersections(binary_sections)
    print(f'Answer to part 1: {answer}')

    answer = count_some_intersection(binary_sections)
    print(f'Answer to part 2: {answer}')

