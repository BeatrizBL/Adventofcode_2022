from helpers import read_file_into_list


def clean_input_strategy(
    lines: list,
    values_mapping: dict = {}
) -> list:
    rounds = [l.split(' ') for l in lines]
    return [[values_mapping.get(s,s) for s in l] for l in rounds]

def evaluate_round_result(shape: int, opponent_shape: int) -> str:
    """Decides whether the provided shape wins the opponent, with
    0 - Rock
    1 - Paper
    2 - Scissors

    Args:
        shape, opponent_shape (int): 0-1 value

    Returns:
        int: '1' if the target shape is the winner, '2' if the opponent
        shape is the winner, 'x' for draws
    """
    if shape == opponent_shape:
        return 'x'
    if shape == (opponent_shape+1)%3:
        return '1'
    return '2'

def compute_tournament_results(
    strategy: list
) -> list:
    """'1' for win, 'x' for draw, '2' for loss"""
    return [evaluate_round_result(s2,s1) for s1,s2 in strategy]

def compute_tournament_score(
    shapes: list,
    results: list,
    shape_score: dict = {0: 1, 1: 2, 2: 3},
    result_score: dict = {'1': 6, 'x': 3, '2': 0}
) -> int:
    shape_total_score = [shape_score.get(s,0) for s in shapes]
    result_total_score = [result_score.get(r) for r in results]
    return sum(shape_total_score) + sum(result_total_score)

def obtain_shape_for_result(
    opponent_shape: int,
    result: str
) -> int:
    """Decides which shape should be used so that the result of
    the match is as indicated.

    Args:
        opponent_shape (int): 0 for Rock, 1 for Paper, 2 for Scissors
        result (str): '1' for win, 'x' for draw, '2' for loss

    Returns:
        int: 0-2 as for the input shape
    """
    return ( opponent_shape + int(result.replace('x', '0')) )%3


if __name__ == '__main__':
    lines = read_file_into_list(path='02_Rock_Paper_Scissors/2_input.txt')

    strategy = clean_input_strategy(
        lines=lines,
        values_mapping={'A': 0, 'B': 1, 'C': 2,
                        'X': 0, 'Y': 1, 'Z': 2}
    )
    answer = compute_tournament_score(
        shapes = [s for _, s in strategy],
        results = compute_tournament_results(strategy)
    )
    print(f'Answer to part 1: {answer}')

    strategy = clean_input_strategy(
        lines=lines,
        values_mapping={'A': 0, 'B': 1, 'C': 2,
                        'X': '2', 'Y': 'x', 'Z': '1'}
    )
    answer = compute_tournament_score(
        shapes = [obtain_shape_for_result(s,r) for s,r in strategy],
        results = [r for _, r in strategy]
    )
    print(f'Answer to part 2: {answer}')
