import numpy as np

def is_non_decreasing(lst):
    return all(x <= y for x, y in zip(lst, lst[1:]))

def monotonicity_value(grid):
    binary_string = ''

    # Check rows for monotonicity
    for row in grid:
        if is_non_decreasing(row):
            binary_string += '1'
        else:
            binary_string += '0'

    # Check columns for monotonicity
    for col in range(len(grid[0])):
        column = [grid[row][col] for row in range(len(grid))]
        if is_non_decreasing(column):
            binary_string += '1'
        else:
            binary_string += '0'

    # Convert binary string to integer
    monotonicity_id = int(binary_string, 2)
    return monotonicity_id

def find_highest_tile(grid):
    max_value = None
    max_index = (None, None)

    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if max_value is None or value > max_value:
                max_value = value
                max_index = (i, j)

    return max_index, int(max_value)

def calculate_fitness(game_stat):
    fitness = 0
    # -MAX_TILE-#  / # -SMOOTHNESS-#
    _,max_tile = find_highest_tile(np.array(game_stat.board))
    fitness += np.log2(max_tile + 1) / calculate_smoothness(
        game_stat.board
    )
    # - SCORE - #
    fitness += np.log2(game_stat.score + 1)
    return fitness


def calculate_smoothness(board):
    """
    Calculate the smoothness of a 2048 game board.

    :param board: A list of 16 integers representing the game board.
    :return: A smoothness score, where a lower score indicates a smoother board.
    """
    board = board.tolist()

    smoothness = 0
    size = 4  # Assuming a 4x4 board

    # Calculate differences between horizontally adjacent tiles
    for row in board:
        for i in range(size - 1):
            if row[i] != 0 and row[i + 1] != 0:  # Only compare non-empty tiles
                smoothness += abs(row[i] - row[i + 1])

    # Calculate differences between vertically adjacent tiles
    for i in range(size):
        for j in range(size - 1):
            if (
                board[j][i] != 0 and board[j + 1][i] != 0
            ):  # Only compare non-empty tiles
                smoothness += abs(board[j][i] - board[j + 1][i])
    if smoothness < 0.1:
        return 1
    return smoothness
if __name__ == "__main__":
    # Example grid
    grid = [[2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]]

    # Get the monotonicity value
    print(monotonicity_value(grid))
