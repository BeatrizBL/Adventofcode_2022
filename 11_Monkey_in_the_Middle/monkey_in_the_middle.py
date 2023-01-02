from helpers import read_file_into_list, compute_least_common_multiple
from math import floor
import re

class Item():

    def __init__(
        self, 
        worry_level: int,
        relief_decrease: int = 3
    ):
        self.worry_level = worry_level
        self._relief_decrease = relief_decrease

    def increase_worry_level(self, level: int):
        if level < self.worry_level:
            raise ValueError(f'New worrying level {level} lower than current {self.worry_level}')
        self.worry_level = level

    def decrease_worry_level(self):
        self.worry_level = floor( self.worry_level / self._relief_decrease )


class Monkey():

    def __init__(
        self, 
        inspect_method: callable,
        test_method: callable,
        test_divisor: int
    ):
        self.items_queue = []
        self.inspect_method = inspect_method
        self.test_method = test_method
        self.test_divisor = test_divisor 
        self.inspected_counter = 0

    def get_next_item(self) -> Item:
        if len(self.items_queue) > 0:
            return self.items_queue.pop(0)    
        return None

    def catch_item(self, item: Item):
        self.items_queue.append(item)

    def inspect_item(self, item: Item):
        new_worry = self.inspect_method(item.worry_level)
        item.increase_worry_level(new_worry)
        item.decrease_worry_level()
        self.inspected_counter += 1

    def throw_item_to(self, item: Item) -> int:
        return self.test_method(item.worry_level)


def _process_starting_items(
    input_items: str,
    relief_decrease: int = 3
) -> list:
    items = re.search('Starting items: (.+?)$', input_items).group(1)
    items = [Item(worry_level=int(v.strip()), relief_decrease=relief_decrease) for v in items.split(',')]
    return items

def _process_inspect_method(input_method: str) -> callable:
    method = re.search('Operation: new = (.+?)$', input_method).group(1)
    if 'old' not in method:
        raise ValueError(f'Unknown format for method "{input_method}"')
    return ( lambda old: eval(method) )

def _process_test_method(inputs: tuple) -> tuple:
    divisor = int(re.search('Test: divisible by (\d+?)$', inputs[0]).group(1))
    monkey_if_true = int(re.search('If true: throw to monkey (\d+?)$', inputs[1]).group(1))
    monkey_if_false = int(re.search('If false: throw to monkey (\d+?)$', inputs[2]).group(1))
    return ( lambda worry: monkey_if_true if worry % divisor == 0 else monkey_if_false ), divisor

def create_monkeys(
    input: list,
    relief_decrease: int = 3
) -> list:
    monkeys = []
    for i, lines in enumerate(input):
        monkey_number, items, inspect, test_condition, test_true, test_false = lines
        if i != int(re.search('Monkey (\d+?)', monkey_number).group(1)):
            raise ValueError('Input monkeys not in order')
        starting_items = _process_starting_items(input_items=items, relief_decrease=relief_decrease)
        inspect_method = _process_inspect_method(input_method=inspect)
        test_method, divisor = _process_test_method(inputs=(test_condition, test_true, test_false))
        monkey = Monkey(
            inspect_method=inspect_method, 
            test_method=test_method,
            test_divisor=divisor
        )
        for item in starting_items:
            monkey.catch_item(item)
        monkeys.append(monkey)        
    return monkeys

def _compute_common_divisor(monkeys) -> int:
    divisors = [m.test_divisor for m in monkeys]
    return compute_least_common_multiple(divisors)

def force_reduce_worry_levels(monkeys):
    cap = _compute_common_divisor(monkeys)
    for m in monkeys:
        for item in m.items_queue:
            item.worry_level = item.worry_level % cap

def play_rounds(
    monkeys: list, 
    n_rounds: int, 
    reduce_worry: bool = False
):
    for _ in range(n_rounds):
        for monkey in monkeys:
            item = monkey.get_next_item()
            while item is not None:
                monkey.inspect_item(item)
                throw_to = monkey.throw_item_to(item)
                monkeys[throw_to].catch_item(item)
                item = monkey.get_next_item()
        if reduce_worry:
            force_reduce_worry_levels(monkeys)


def print_monkey_items(monkeys: list):
    for i, monkey in enumerate(monkeys):
        line = f'Monkey {i}: '
        worries = [str(item.worry_level) for item in monkey.items_queue]
        line += ', '.join(worries)
        print(line)

def compute_monkey_business(monkeys: list) -> int:
    activity = sorted([m.inspected_counter for m in monkeys], reverse=True)
    return activity[0] * activity[1]


if __name__ == '__main__':
    input = read_file_into_list(
        path='11_Monkey_in_the_Middle/11_input.txt',
        split_list_char='\n'
    )

    monkeys = create_monkeys(input)
    play_rounds(monkeys, n_rounds=20)
    answer = compute_monkey_business(monkeys)
    print(f'Answer to part 1: {answer}')

    monkeys = create_monkeys(input, relief_decrease = 1)
    play_rounds(monkeys, n_rounds=10000, reduce_worry=True)
    answer = compute_monkey_business(monkeys)
    print(f'Answer to part 2: {answer}')
