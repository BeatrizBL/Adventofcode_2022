from helpers import read_file_into_list, print_sparse_matrix
from copy import deepcopy

class Rock():

    def __init__(
        self, 
        rock_lines: list,
        rock_char: str = '#',
        rock_id: int = None
    ):
        self.pos = self.process_rock_lines(
            lines=rock_lines, rock_char=rock_char
        )
        self.id = rock_id
        self.resting = False

    @staticmethod
    def process_rock_lines(
        lines: list,
        rock_char: str = '#'
    ) -> list:
        # Positions from bottom left (0,0)
        h = len(lines) - 1
        pos = []
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == rock_char:
                    pos.append((x, h-y))
        return pos

    def move_rock(self, dir: str):
        if dir == 'R':
            self.pos = [(x+1,y) for x,y in self.pos]
        elif dir == 'L':
            self.pos = [(x-1,y) for x,y in self.pos]
        elif dir == 'D':
            self.pos = [(x,y-1) for x,y in self.pos]
        elif dir == 'U':
            self.pos = [(x,y+1) for x,y in self.pos]
        else:
            raise ValueError(f'Unknown direction command {dir}')

    def update_rock_reference(self, new_pos: tuple):
        self.pos = [(x+new_pos[0], y+new_pos[1]) for x,y in self.pos]


class Chamber():

    def __init__(
        self, 
        jets: str,
        chamber_width: int = 7,
        rock_start_offset: tuple = (2, 3),
        verbose: bool = False
    ):
        self.chamber_width = chamber_width
        self.jets = jets
        self._jet_index = 0
        self._chamber_dict = {}
        self.rocks = []
        self.max_resting_position = -1
        self.rock_start_offset = rock_start_offset
        self._resting_id = -1
        self.verbose = verbose

    def add_rock(self, rock: Rock):
        corner_x = self.rock_start_offset[0]
        corner_y = self.rock_start_offset[1] + self.max_resting_position + 1
        rock.id = len(self.rocks)
        rock.update_rock_reference((corner_x, corner_y))
        self.update_rock_pos(rock)

    def update_rock_pos(self, rock: Rock):
        self._chamber_dict = {p:r for p,r in self._chamber_dict.items() if r!=rock.id}
        for p in rock.pos:
            self._chamber_dict[p] = rock.id if not rock.resting else self._resting_id
        if self.verbose:
            print_sparse_matrix({(-y,x): '@' if v>=0 else '#' for (x,y),v in self._chamber_dict.items()})
            print('\n')

    def _check_valid_position(self, rock: Rock) -> bool:
        out = [p for p in rock.pos if p[0]<0 or p[0]>=self.chamber_width or p[1]<0]
        overlap = [p for p in rock.pos if self._chamber_dict.get(p,rock.id) != rock.id]
        return len(out+overlap) == 0

    def _move_rock_jet(self, rock: Rock):
        dir = self.jets[self._jet_index]
        self._jet_index = (self._jet_index + 1) % len(self.jets)
        rock.move_rock('R' if dir=='>' else 'L')
        if self._check_valid_position(rock):
            self.update_rock_pos(rock)
        else:
            rock.move_rock('L' if dir=='>' else 'R')

    def _move_rock_down(self, rock: Rock) -> bool:
        # Bool whether the movement actually happened
        moved = False
        if not rock.resting:
            rock.move_rock('D')
            if not self._check_valid_position(rock):
                rock.move_rock('U')
                rock.resting = True
                top = max([y for _,y in rock.pos])
                self.max_resting_position = max(self.max_resting_position, top)
            else:
                moved = True
            self.update_rock_pos(rock)
        return moved

    def move_rock(self, rock: Rock):
        resting = rock.resting
        while not resting:
            self._move_rock_jet(rock)
            resting = not self._move_rock_down(rock)


def drop_rocks(
    chamber: Chamber,
    rocks: list,
    n_rocks: int
):
    for i in range(n_rocks):
        rock = deepcopy(rocks[i%len(rocks)])
        chamber.add_rock(rock)
        chamber.move_rock(rock)


if __name__ == '__main__':
    rocks = read_file_into_list(path='17_Pyroclastic_Flow/rocks.txt', split_list_char='\n')
    rocks = [Rock(r) for r in rocks]

    input = read_file_into_list(path='17_Pyroclastic_Flow/17_input.txt')
    chamber = Chamber(input[0])
    drop_rocks(chamber=chamber, rocks=rocks, n_rocks=2022)
    answer = chamber.max_resting_position + 1
    print(f'Answer to part 1: {answer}')

    answer = None
    print(f'Answer to part 2: {answer}')
