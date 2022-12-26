from helpers import read_file_into_list


def aggregate_elf_calories(cal: list) -> int:
    return [sum([int(s) for s in l]) for l in cal]

def max_elf_calories(cal: list) -> int:
    return max(aggregate_elf_calories(cal=cal))

def total_top_elf_calories(cal: list, top_n: int) -> int:
    top_cal = sorted(aggregate_elf_calories(cal=cal), reverse=True)
    return sum(top_cal[:top_n])


if __name__ == '__main__':
    cal = read_file_into_list(
        path='1_Calorie_Counting/1_input.txt',
        split_list_char='\n'
    )
    answer = max_elf_calories(cal)
    print(f'Answer to part 1: {answer}')

    answer = total_top_elf_calories(cal, top_n=3)
    print(f'Answer to part 2: {answer}')

