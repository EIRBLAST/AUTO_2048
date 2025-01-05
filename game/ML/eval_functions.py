import numpy as np
import math

import math

import math

def calculate_smoothness(board):
    """
    Calculate smoothness using logarithmic scaling and normalization.
    Higher is better.
    bounds : [0 : -infinity]
    """
    smoothness = 0
    for i in range(4):
        for j in range(4):
            if j < 3:  # Horizontal neighbor
                if board[i][j] > 0 and board[i][j + 1] > 0:
                    log_diff = abs(math.log2(board[i][j]) - math.log2(board[i][j + 1]))
                    max_log = max(math.log2(board[i][j]), math.log2(board[i][j + 1]))
                    smoothness -= log_diff / max_log
            if i < 3:  # Vertical neighbor
                if board[i][j] > 0 and board[i + 1][j] > 0:
                    log_diff = abs(math.log2(board[i][j]) - math.log2(board[i + 1][j]))
                    max_log = max(math.log2(board[i][j]), math.log2(board[i + 1][j]))
                    smoothness -= log_diff / max_log
    return smoothness



def calculate_monotonicity(board):
    monotonicity = 0
    
    # Row-wise monotonicity
    for i in range(4):
        row = board[i]
        for j in range(3):
            if row[j] > row[j + 1]:  # Decreasing
                monotonicity += row[j + 1] - row[j]
            elif row[j] < row[j + 1]:  # Increasing
                monotonicity += row[j] - row[j + 1]
    
    # Column-wise monotonicity
    for j in range(4):
        for i in range(3):
            if board[i][j] > board[i + 1][j]:  # Decreasing
                monotonicity += board[i + 1][j] - board[i][j]
            elif board[i][j] < board[i + 1][j]:  # Increasing
                monotonicity += board[i][j] - board[i + 1][j]
    
    return monotonicity

def calculate_directional_monotonicity(board):
    scores = [0, 0, 0, 0]  # Row-increasing, Row-decreasing, Col-increasing, Col-decreasing
    
    # Row-wise monotonicity
    for i in range(4):
        for j in range(3):
            if board[i][j] <= board[i][j + 1]:  # Row-increasing
                scores[0] += board[i][j + 1] - board[i][j]
            if board[i][j] >= board[i][j + 1]:  # Row-decreasing
                scores[1] += board[i][j] - board[i][j + 1]
    
    # Column-wise monotonicity
    for j in range(4):
        for i in range(3):
            if board[i][j] <= board[i + 1][j]:  # Col-increasing
                scores[2] += board[i + 1][j] - board[i][j]
            if board[i][j] >= board[i + 1][j]:  # Col-decreasing
                scores[3] += board[i][j] - board[i + 1][j]
    
    return scores

def calculate_total_monotonicity(board):
    scores = calculate_directional_monotonicity(board)
    total_score = sum(scores)
    return total_score

def evaluate_board(board):
    """
    Evaluate a 2048 board based on its features.
    """
    board = board.tolist()

    # Calculate individual features
    smoothness = calculate_smoothness(board)
    monotonicity = calculate_total_monotonicity(board)
    empty_tiles = sum(1 for row in board for cell in row if cell == 0)
    max_tile = max(max(row) for row in board)
    max_tile = 0 if max_tile == 0 else math.log2(max_tile)
    # Weight each feature (adjust weights based on testing)
    smoothness_weight = 1.0
    monotonicity_weight = 1.5
    empty_tiles_weight = 2.0
    max_tile_weight = 1.0

    # Combine features into a single score
    score = (
        smoothness_weight * smoothness +
        monotonicity_weight * monotonicity +
        empty_tiles_weight * empty_tiles +
        max_tile_weight * max_tile
    )
    return score

if __name__ == "__main__":
    # Example grid
    gridSmooth = np.array([[2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]])
    gridNoSmooth = np.array([[2,4,4,2],
                    [4,8,16,32],
                    [2048,4,2,64],
                    [2,4,4,2]])
    gridZero = np.zeros((4,4),int)
    # Get the monotonicity value
    print(calculate_total_monotonicity(gridZero))
    print(calculate_total_monotonicity(gridNoSmooth))
    print(calculate_total_monotonicity(gridSmooth))
