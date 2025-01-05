from ML.ppo import PPOModel
from ML.train import train_ppo
from ML.eval_functions import evaluate_board as calculate_fitness

import torch
import torch.optim as optim
from game_2048 import Game
from pathlib import Path

# Main script for training
if __name__ == "__main__":
    # Hyperparameters
    num_episodes = 1000
    gamma = 0.99
    learning_rate = 1e-4
    clip_eps = 0.2
    save_path = Path("best_ppo_model.pth")

    # Initialize model and optimizer
    model = PPOModel()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    best_score = 0

    for episode in range(num_episodes):
        # Train the model
        env = Game(draw=False)
        env.add_new_tile()
        env.add_new_tile()

        train_ppo(env, model, optimizer, gamma=gamma, clip_eps=clip_eps)

        # Evaluate performance
        final_score = calculate_fitness(env.board)
        if final_score > best_score:
            best_score = final_score
            torch.save(model.state_dict(), save_path)  # Save the best model
            print(f"Episode {episode}: New best score {best_score}")

    print("Training complete. Best model saved to:", save_path)
