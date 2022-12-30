
from helpers import read_file_into_list
from graph import Tree

class FileSystem():

    def __init__(self):
        self._fs = self._initialize_fs()
        self._cwd = '/'
        self._directories = ['/']

    def _initialize_fs(self) -> Tree:
        fs = Tree()
        fs.add_update_node('/')
        return fs

    def getcwd(self) -> str:
        return self._cwd

    def chdir(self, new_dir):
        if new_dir == '..':
            self._cwd = self._fs.get_parent_node(self._cwd)
        elif new_dir == '/':
            self._cwd = '/'
        else:
            name = self._name(new_dir)
            if name not in self._fs.get_child_nodes(self._cwd):
                raise ValueError(f'{new_dir} not found in current directory, {self._cwd}')
            self._cwd = name

    def _name(self, name: str) -> str:
        """Absolute path"""
        if name.startswith('/'):
            return name 
        if self._cwd == '/':
            return '/' + name
        return self._cwd + '/' + name

    def _add_element(self, name: str, size: int = None):
        name = self._name(name)
        if name in self._fs.get_child_nodes(self._cwd):
            raise ValueError(f'{name} already in {self._cwd}')
        self._fs.add_update_node(node=name, value=size)
        self._fs.add_edge(self._cwd, name)

    def add_file(self, file_name: str, size: int):
        self._add_element(name=file_name, size=size)

    def create_directory(self, dir_name: str):
        self._add_element(name=dir_name)
        self._directories.append(self._name(dir_name))

    def get_directories(self) -> list:
        return self._directories

    def get_element_size(self, name: str) -> int:
        """Recursive method to compute the total size of an element"""
        name = self._name(name)
        if self._fs.get_node(name) is not None:
            return self._fs.get_node(name)
        size = 0
        for e in self._fs.get_child_nodes(name):
            size += self.get_element_size(e)
        self._fs.add_update_node(node=name, value=size)
        return size


def process_command_lines(input: list) -> list:
    """Process the command lines into a list of tuples where
    - the first element is the command
    - and the second element is the output of each command, as a list of lines.
    """
    processed = {}
    commands_ix = [i for i in range(len(input)) if input[i].startswith('$')]
    if 0 not in commands_ix:
        raise ValueError(f'First line is not a command - {input[0]}')
    commands_ix = commands_ix + [len(input)]
    processed = [(input[i],input[(i+1):j]) \
        for i,j in zip(commands_ix[:(len(commands_ix)-1)], commands_ix[1:])]
    return processed

def build_file_system(command_lines: list) -> FileSystem:
    fs = FileSystem()
    for command, output in command_lines:
        if '$ cd' in command:
            fs.chdir(command.split('$ cd')[1].strip())
        elif '$ ls' in command:
            for element in output:
                if element.startswith('dir'):
                    name = element.split(' ')[1]
                    fs.create_directory(dir_name=name)
                else:
                    size, name = element.split(' ')
                    fs.add_file(file_name=name, size=int(size))
        else:
            raise ValueError(f'Command unknown - {command}')
    return fs

def compute_total_directory_size(
    fs: FileSystem, 
    maximum_size: int = None
) -> int:
    sizes = [fs.get_element_size(d) for d in fs.get_directories()]
    if maximum_size is not None:
        sizes = [s for s in sizes if s<=maximum_size]
    return sum(sizes)

def get_directory_to_delete(
    fs: FileSystem, 
    total_size: int,
    size_required: int
) -> int:
    free = total_size - fs.get_element_size('/')
    if free >= size_required:
        return 0
    size_to_free = size_required - free
    sizes = [fs.get_element_size(d) for d in fs.get_directories()]
    sizes = [s for s in sizes if s>=size_to_free]
    return min(sizes)


if __name__ == '__main__':
    instructions = read_file_into_list(path='7_No_Space_Left_On_Device/7_input.txt')
    instructions = process_command_lines(instructions)
    filesystem = build_file_system(command_lines=instructions)

    answer = compute_total_directory_size(filesystem, maximum_size=100000)
    print(f'Answer to part 1: {answer}')

    answer = get_directory_to_delete(
        filesystem, 
        total_size=70000000,
        size_required=30000000
    )
    print(f'Answer to part 2: {answer}')
