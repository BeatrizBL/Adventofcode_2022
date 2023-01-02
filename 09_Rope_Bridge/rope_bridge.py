from helpers import read_file_into_list

class Rope():

    def __init__(self):
        self.head_positions = {(0,0): 1}
        self.tail_positions = {(0,0): 1}
        self.current_head = (0,0)
        self.current_tail = (0,0)

    @property
    def are_adjacent(self) -> bool:
        dist = [a-b for a,b in zip(self.current_head, self.current_tail)]
        return max([abs(d) for d in dist]) <= 1

    @staticmethod
    def process_direction(position: tuple, direction: str) -> tuple:
        i, j = position
        if direction == 'U':
            return (i-1, j)
        if direction == 'R':
            return (i, j+1)
        if direction == 'D':
            return (i+1, j)
        if direction == 'L':
            return (i, j-1)
        raise ValueError(f'Unknown direction {direction}')

    def _compute_next_tail_position(self) -> tuple:
        if self.are_adjacent:
            return self.current_tail
        hi, hj = self.current_head
        ti, tj = self.current_tail
        return ( ti + max(min(hi-ti, 1), -1), tj + max(min(hj-tj, 1), -1) )

    def _update_head_position(self, new_position: tuple):
        self.head_positions[self.current_head] = 0
        self.current_head = new_position
        self.head_positions[self.current_head] = 1

    def _update_tail_position(self, new_position: tuple):
        self.tail_positions[self.current_tail] = 0
        self.current_tail = new_position
        self.tail_positions[self.current_tail] = 1

    def _update_tail(self):
        if not self.are_adjacent:
            new_position = self._compute_next_tail_position()
            self._update_tail_position(new_position)

    def update_positions(self, new_head: tuple):
        self._update_head_position(new_head)
        self._update_tail()

    def move_step(self, direction: str):
        new_head = self.process_direction(self.current_head, direction)
        self.update_positions(new_head)

    @staticmethod
    def print_positions(
        pos: dict, 
        mark_path: bool = False,
        main_chars: list = []
    ):
        y1 = min([i for i,_ in list(pos.keys())])
        y2 = max([i for i,_ in list(pos.keys())])
        x1 = min([j for _,j in list(pos.keys())])
        x2 = max([j for _,j in list(pos.keys())])
        for i in range(y1, y2+1):
            line = ''
            for j in range(x1, x2+1):
                c = pos.get((i,j), None)
                if c not in main_chars:
                    if i == 0 and j == 0:
                        line += 's'
                    elif mark_path and c is not None:
                        line += '#'
                    else:
                        line += '.'
                else:
                    line += c
            print(line)

    def print_head_path(self):
        self.print_positions(
            pos = {k: ('.' if v==0 else 'H') for k,v in self.head_positions.items()},
            mark_path = True,
            main_chars = ['H']
        )

    def print_tail_path(self):
        self.print_positions(
            pos = {k: ('.' if v==0 else 'T') for k,v in self.tail_positions.items()},
            mark_path = True,
            main_chars = ['T']
        )

    def print_current_positions(self):
        pos = {k: ('.' if v==0 else 'T') for k,v in self.tail_positions.items()}
        for k,v in self.head_positions.items():
            pos[k] = ('H' if v==1 else ('T' if pos.get(k,'')=='T' else '.'))
        self.print_positions(
            pos = pos,
            mark_path = False,
            main_chars = ['H', 'T']
        )
        

class RopeGroup():

    def __init__(self, n_tails: int):
        self.head_rope = Rope()
        self.ropes = [Rope() for _ in range(n_tails)]

    def move_step(self, direction: str):
        self.head_rope.move_step(direction)
        prev_tail = self.head_rope.current_tail
        for i in range(len(self.ropes)):
            self.ropes[i].update_positions(new_head=prev_tail)
            prev_tail = self.ropes[i].current_tail

    def print_current_positions(self):
        rope_chars = ['H'] + [str(i+1) for i in range(len(self.ropes))]
        pos = {k: ('.' if v==0 else 'H') for k,v in self.head_rope.head_positions.items()}
        for i in range(len(self.ropes)):
            for k,v in self.ropes[i].head_positions.items():
                pos[k] = (pos.get(k,'') if pos.get(k,'') in rope_chars else (str(i+1) if v==1 else '.'))
        Rope().print_positions(
            pos = pos,
            mark_path = False,
            main_chars = rope_chars
        )


def expand_input_directions(input: list) -> list:
    directions = [s.split(' ') for s in input]
    directions = [[d] * int(n) for d, n in directions]
    return [v for l in directions for v in l]

def move_ropes(
    rope, 
    directions: list,
    verbose: bool = False
) -> Rope:
    for d in directions:
        rope.move_step(d)
        if verbose:
            rope.print_current_positions()
            print('\n')
    return rope


if __name__ == '__main__':
    input = read_file_into_list(path='09_Rope_Bridge/9_input.txt')
    directions = expand_input_directions(input)

    rope = Rope()
    rope = move_ropes(rope, directions)
    answer = len(rope.tail_positions)
    print(f'Answer to part 1: {answer}')

    n_tails = 9
    rope_group = RopeGroup(n_tails=n_tails)
    rope_group = move_ropes(rope_group, directions)
    answer = len(rope_group.ropes[n_tails-1].head_positions)
    print(f'Answer to part 2: {answer}')
