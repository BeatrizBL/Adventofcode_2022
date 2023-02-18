from helpers import read_file_into_list
from sympy import symbols, solve, Eq


def process_input(input: list) -> dict:
    return {s.split(':')[0]: s.split(':')[1].strip() for s in input}

def build_expression(monkeys: dict, start: str = 'root') -> str:
    if monkeys[start].isdigit():
        return monkeys[start]
    else:
        parts = monkeys[start].split(' ')
        m1 = parts[0].strip()
        op = parts[1].strip()
        m2 = parts[2].strip()
        return f'({build_expression(monkeys, m1)} {op} {build_expression(monkeys, m2)})'

def build_equality(
    monkeys: dict, 
    start: str = 'root',
    variable: str = 'humn',
    id_value: float = '1000' # Number that is not in the input
) -> str:
    monkeys_adj = monkeys.copy()
    monkeys_adj[variable] = id_value
    parts = monkeys[start].split(' ')
    eqs = []
    for i in [0,-1]:
        p = parts[i].strip()
        eq = build_expression(monkeys=monkeys_adj, start=p)
        eq = eq.replace(id_value, 'x')
        eqs.append(eq)
    eq = f'({eqs[0]}) - ({eqs[1]})'
    return eq

def process_equality(
    monkeys: dict, 
    start: str = 'root',
    variable: str = 'humn'
) -> int:
    eq = build_equality(monkeys, start, variable)
    x = symbols('x')
    return solve(Eq(eval(eq)))[0]


if __name__ == '__main__':
    input = read_file_into_list(path='21_Monkey_Math/21_input.txt')
    monkeys = process_input(input)

    answer = int(eval(build_expression(monkeys)))
    print(f'Answer to part 1: {answer}')

    answer = int(process_equality(monkeys))
    print(f'Answer to part 2: {answer}')
