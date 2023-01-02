from helpers import read_file_into_list

class CPU():

    def __init__(
        self, 
        signal_cycle_start: int = 20,
        signal_cycle_length: int = 40
    ):
        self.clock = 1
        self.X = [1]
        self.signal_cycle_start = signal_cycle_start
        self.signal_cycle_length = signal_cycle_length
        self.signals = []

    def register_signal(self):
        if ( self.clock % self.signal_cycle_length - self.signal_cycle_start ) == 0:
            self.signals.append((self.clock, self.X[-1]))

    def addx(self, v: int):
        for i in range(2):
            self.clock += 1
            if i == 0:
                self.X.append(self.X[-1])
            else:
                self.X.append(self.X[-1] + v)
            self.register_signal()

    def noop(self):
        self.clock += 1
        self.X.append(self.X[-1])
        self.register_signal()

    @property
    def signal_strengths(self) -> list:
        return [i*v for i,v in self.signals]

    def run_CPU_program(self, instructions: list):
        for s in instructions:
            if s == 'noop':
                self.noop()
            elif s.startswith('addx'):
                v = int(s.split('addx')[1].strip())
                self.addx(v)
            else:
                raise ValueError(f'Unknown instruction - {s}')


class CRT():

    def __init__(
        self, 
        screen_width: int = 40,
        screen_height: int = 6
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = ['.']*(screen_height * screen_width)
        self.cpu = CPU(signal_cycle_start=0, signal_cycle_length=screen_width)

    def _update_screen(self):
        for cycle in range(len(self.screen)):
            sprite = self.cpu.X[cycle]
            crt = cycle % self.screen_width
            if crt >= (sprite-1) and crt <= (sprite+1):
                self.screen[cycle] = '#'

    def run_program(self, instructions: list):
        self.cpu.run_CPU_program(instructions)
        self._update_screen()

    def print_screen(self):
        n = self.screen_width
        for line in [self.screen[i:(i+n)] for i in range(0,len(self.screen),n)]:
            print(''.join(line))


if __name__ == '__main__':
    instructions = read_file_into_list(path='10_Cathode_Ray_Tube/10_input.txt')
    cpu = CPU()
    cpu.run_CPU_program(instructions)

    answer = sum(cpu.signal_strengths)
    print(f'Answer to part 1: {answer}')

    crt = CRT()
    crt.run_program(instructions)
    print(f'Answer to part 2:')
    crt.print_screen()
