from helpers import read_file_into_list, print_sparse_matrix
from copy import deepcopy
import altair as alt
from pandas import DataFrame
import imageio
import os

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
        verbose: bool = False,
        save_all_steps: bool = False
    ):
        self.chamber_width = chamber_width
        self._chamber_dict = {}
        self.jets = jets
        self.jet_index = 0

        self.rocks = []
        self.rock_start_offset = rock_start_offset
        self.max_resting_position = -1
        self._resting_tag = -1 # Mark used for resting rocks value in dict

        self.verbose = verbose
        self.save_all_steps = save_all_steps
        self._all_steps = []


    def add_rock(self, rock: Rock):
        corner_x = self.rock_start_offset[0]
        corner_y = self.rock_start_offset[1] + self.max_resting_position + 1
        rock.id = len(self.rocks)
        rock.update_rock_reference((corner_x, corner_y))
        self.update_rock_pos(rock)

    def update_rock_pos(self, rock: Rock):
        self._chamber_dict = {p:r for p,r in self._chamber_dict.items() if r!=rock.id}
        for p in rock.pos:
            self._chamber_dict[p] = rock.id if not rock.resting else self._resting_tag
        if self.verbose:
            print_sparse_matrix({(-y,x): '@' if v>=0 else '#' for (x,y),v in self._chamber_dict.items()})
            print('\n')
        if self.save_all_steps:
            self._all_steps.append(self._chamber_dict.copy())

    def _check_valid_position(self, rock: Rock) -> bool:
        out = [p for p in rock.pos if p[0]<0 or p[0]>=self.chamber_width or p[1]<0]
        overlap = [p for p in rock.pos if self._chamber_dict.get(p,rock.id) != rock.id]
        return len(out+overlap) == 0

    def _move_rock_jet(self, rock: Rock):
        dir = self.jets[self.jet_index]
        self.jet_index = (self.jet_index + 1) % len(self.jets)
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

    def _generate_images(self, steps: list) -> list:
        max_y = max([y for d in steps for _,y in d.keys()])
        images = []
        for d in steps:
            data = DataFrame([{
                'x': x, 'y': y, 
                'color': 1 if v<0 else 0,
                'size': 1
            } for (x,y),v in d.items()])
            fig = alt.Chart(data).mark_square().encode(
                x=alt.X(
                    'x:N', scale=alt.Scale(domain=list(range(self.chamber_width))),
                    axis=alt.Axis(labels=False, tickSize=0),
                    title=''
                ),
                y=alt.Y(
                    'y:N', scale=alt.Scale(reverse=True, domain=list(range(max_y+1))),
                    axis=alt.Axis(labels=False, tickSize=0),
                    title=''
                ),
                color=alt.Color(
                    'color:N', 
                    scale=alt.Scale(domain=[0,1], range=['blue', 'grey']),
                    legend=None
                ),
                size=alt.Size('size', legend=None)
            )
            images.append(fig)
        return images

    def store_moves_gif(
        self,
        n_steps: int = 50,
        file_name: str = '17_Pyroclastic_Flow/chamber.gif'
    ):
        if len(self._all_steps) == 0:
            raise ValueError('No movements to display')
        images = self._generate_images(self._all_steps[:n_steps])
        byte_images = []
        for image in images:
            image.save('_temp.png')
            byte_images.append(imageio.imread('_temp.png'))
        imageio.mimsave(file_name, byte_images, duration=0.3)
        os.remove('_temp.png')

    @property
    def bottom_profile(self) -> str:
        def _blocked(x,y) -> bool:
            return (self._chamber_dict.get((x, y), None) == self._resting_tag) or (y<0)
        bottom_rocks_pos = [p for p, v in self._chamber_dict.items() if v == self._resting_tag and p[1]==0]
        left_rocks_pos = [p for p, v in self._chamber_dict.items() if v == self._resting_tag and p[0]==0]
        if len(bottom_rocks_pos) == 0:
            return '>'*self.chamber_width # No rock at the bottom
        if len(left_rocks_pos) == 0:
            x, y = min(bottom_rocks_pos, key=lambda p: p[0])
            x = x-1
            profile = '>'*x
        else:
            x, y = max(left_rocks_pos, key=lambda p: p[1])
            y = y+1
            profile = ''

        direction_tags = ['>', 'v', '<', '^']
        directions = [(1,0), (0,-1), (-1,0), (0,1)]
        dir = 0
        while x != self.chamber_width:
            # Try to turn to the right
            turn_dir = (dir+1) % len(directions)
            if not _blocked(x+directions[turn_dir][0], y+directions[turn_dir][1]):
                dir = turn_dir
            elif _blocked(x+directions[dir][0], y+directions[dir][1]):
                # If current direction is blocked, turn anticlockwise
                dir = (dir-1) % len(directions)
                while _blocked(x+directions[dir][0], y+directions[dir][1]):
                    dir = (dir-1) % len(directions)
            x, y = x+directions[dir][0], y+directions[dir][1]
            profile = profile + direction_tags[dir]
        return profile



def drop_rocks(
    chamber: Chamber,
    rocks: list,
    n_rocks: int
):
    for i in range(n_rocks):
        rock = deepcopy(rocks[i%len(rocks)])
        chamber.add_rock(rock)
        chamber.move_rock(rock)



def find_drop_cycle_positions(
    chamber: Chamber,
    rocks: list,
    n_rocks: int
) -> tuple:
    def _state_hash(rock_ix: int, jet_ix: int, profile: str) -> str:
        return str(rock_ix) + '-' + str(jet_ix) + '-' + profile
    state_records = []
    high_records = []
    idx = 0
    for i in range(n_rocks):
        rock_index = i % len(rocks)
        rock = deepcopy(rocks[rock_index])
        chamber.add_rock(rock)
        chamber.move_rock(rock)
        state = _state_hash(rock_index, chamber.jet_index, chamber.bottom_profile)
        if state in state_records:
            idx = state_records.index(state)
            break
        state_records.append(state)
        high_records.append(chamber.max_resting_position + 1)
    return (idx, i), high_records + [chamber.max_resting_position + 1]

def simulate_drop_rocks(
    chamber: Chamber,
    rocks: list,
    n_rocks: int
):
    (first_start, second_start), heights = find_drop_cycle_positions(chamber, rocks, n_rocks)
    previous_height = heights[first_start]
    cycle_length = second_start - first_start
    cycle_height = heights[second_start] - heights[first_start]
    n_iters = int( (n_rocks - first_start) / cycle_length )
    after_iters = (n_rocks - first_start) % cycle_length
    if after_iters > 0:
        after_height = (heights[first_start+after_iters-1] - heights[first_start])
    elif after_iters == 0:
        after_height =  heights[first_start-1] - heights[first_start] if first_start > 0 else 0
    return previous_height + cycle_height * n_iters + after_height



if __name__ == '__main__':
    rocks = read_file_into_list(path='17_Pyroclastic_Flow/rocks.txt', split_list_char='\n')
    rocks = [Rock(r) for r in rocks]

    input = read_file_into_list(path='17_Pyroclastic_Flow/17_input.txt')
    chamber = Chamber(input[0])
    # chamber.save_all_steps = True
    drop_rocks(chamber=chamber, rocks=rocks, n_rocks=2022)
    # chamber.store_moves_gif(n_steps=110)

    answer = chamber.max_resting_position + 1
    print(f'Answer to part 1: {answer}')

    chamber = Chamber(input[0])
    answer = simulate_drop_rocks(chamber=chamber, rocks=rocks, n_rocks=1000000000000)
    print(f'Answer to part 2: {answer}')
