from ML.ppo import PPOModel
from ML.eval_functions import evaluate_board as calculate_fitness
from game_2048 import Game

import torch
import pygame
import numpy as np

# Direction mappings for actions
directions = {0: [0, -1], 1: [0, 1], 2: [1, 0], 3: [-1, 0]}

# Preprocess the game board for input
def preprocess_board(board):
    """
    Normalize the game board for neural network input.
    Convert tiles to log2 values and scale to [0, 1].
    """
    return np.log2(np.array(board, dtype=np.float32) + 1) / 16  # Normalize by 16 (max tile exponent for 65536)


if __name__ == "__main__":
    # Path to the saved model
    model_path = "best_ppo_model.pth"

    # Load the trained model
    model = PPOModel()
    model.load_state_dict(torch.load(model_path))
    model.eval()

    print("Loaded model. Starting test game.")
    
    clock = pygame.time.Clock()
    # Play a game with the trained model
    pygame.init()
    env = Game(draw=True)
    env.add_new_tile()
    env.add_new_tile()

    while env.is_on():
        clock.tick(60)
        state = preprocess_board(env.board)
        state_tensor = torch.tensor(state).unsqueeze(0).unsqueeze(0)
        policy, _ = model(state_tensor)

        # Select the action with the highest probability
        action = torch.argmax(policy).item()
        move = directions.get(action)
        env.update(move[0], move[1])
        env.check_game_state()

    print(f"Game over! Final score: {calculate_fitness(env)}")
