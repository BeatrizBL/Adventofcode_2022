from helpers import read_file_into_list
from math import log, floor

def snafu_to_decimal(
    snafu: str, 
    base: int = 5,
    digit_map: dict = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
) -> int:
    return sum([digit_map[s] * (base ** i) for i, s in enumerate(snafu[::-1])])

def sum_snafus(snafus: list) -> int:
    return sum([snafu_to_decimal(s) for s in snafus])

def decimal_to_snafu(n: int) -> str:
    base = 5
    digits = floor(log(n, base))
    l = []
    rest = n
    # Transform to base 5
    for i in range(digits+1, -1, -1):
        c = floor(rest / (base ** i))
        rest = rest % (base ** i)
        l.append(c)
    # Replace numbers over 2 by symbols & adjust
    for i in range(digits+1, 0, -1):
        if l[i] > 4:
            l[i-1] += floor(l[i] / 5)
            l[i] = (l[i] % 5)
        if l[i] > 2:
            l[i] = '-' if l[i] == 4 else '='
            l[i-1] += 1
        else:
            l[i] = str(l[i])
    l[0] = str(l[0])
    l = l[1:] if l[0] == '0' else l
    return ''.join(l)

if __name__ == '__main__':
    input = read_file_into_list(path='25_Full_of_Hot_Air/25_input.txt')
    answer = decimal_to_snafu(sum_snafus(input))
    print(f'Answer to part 1: {answer}')
