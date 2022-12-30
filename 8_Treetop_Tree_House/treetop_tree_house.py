from helpers import read_file_into_list
import numpy as np

def process_input_trees(input: list) -> np.array:
    trees = [[int(c) for c in s] for s in input]
    return np.array(trees)

def is_tree_visible(trees: np.array, tree_ix: tuple) -> bool:
    i, j = tree_ix
    height = trees[i, j]
    return ( height > trees[i,:j].max() or # left
             height > trees[i,(j+1):].max() or # right
             height > trees[:i,j].max() or # up
             height > trees[(i+1):,j].max() ) # down

def count_visible_trees(trees) -> int:
    visible = 4 * ( len(trees) - 1 ) # Edge trees
    for i in range(1, len(trees)-1):
        for j in range(1, len(trees)-1):
            if is_tree_visible(trees, (i,j)):
                visible += 1
    return visible

def compute_scenic_score(trees: np.array, tree_ix: tuple) -> int:
    i, j = tree_ix
    if i == 0 or j == 0 or i == len(trees) or j == len(trees):
        return 0
    height = trees[i, j]
    left = np.flip(trees[i,:j])
    right = trees[i,(j+1):]
    up = np.flip(trees[:i,j])
    down = trees[(i+1):,j]
    score = 1
    for line in [left, right, up, down]:
        if line.max() >= height:
            line = line[:(np.argmax(line>=height)+1)] # Up to first >= element
        score = score * len(line)
    return score

def compute_max_scenic_score(trees) -> int:
    max_score = 0
    for i in range(1, len(trees)-1):
        for j in range(1, len(trees)-1):
            score = compute_scenic_score(trees, (i,j))
            if score > max_score:
                max_score = score
    return max_score      

if __name__ == '__main__':
    trees = read_file_into_list(path='8_Treetop_Tree_House/8_input.txt')
    trees = process_input_trees(trees)

    answer = count_visible_trees(trees)
    print(f'Answer to part 1: {answer}')

    answer = compute_max_scenic_score(trees)
    print(f'Answer to part 2: {answer}')
