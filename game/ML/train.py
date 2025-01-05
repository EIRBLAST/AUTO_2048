import torch
import torch.nn.functional as F
import numpy as np
from torch.distributions import Categorical
from eval_functions import evaluate_board as calculate_fitness

directions = {0:[0,-1],1:[0,1],2:[1,0],3:[-1,0]}
location = {
    (0, 0):0,
    (0, 1):0,
    (0, 2):1,
    (0, 3):1,
    (1, 0):0,
    (1, 1):0,
    (1, 2):1,
    (1, 3):1,
    (2, 0):2,
    (2, 1):2,
    (2, 2):3,
    (2, 3):3,
    (3, 0):2,
    (3, 1):2,
    (3, 2):3,
    (3, 3):3
}

def preprocess_board(board):
    """
    Normalize the game board for neural network input.
    Convert tiles to log2 values and scale to [0, 1].
    """
    return np.log2(np.array(board, dtype=np.float32) + 1) / 16  # Normalize by 16 (max tile exponent for 65536)

def train_ppo(env, model, optimizer, gamma=0.99, clip_eps=0.2, epochs=10, batch_size=32):
    """
    Train PPO agent.
    """
    # Storage for training
    states, actions, rewards, dones, log_probs, values = [], [], [], [], [], []

    # Run an episode
    state = preprocess_board(env.board)
    done = False
    while not done:
        state_tensor = torch.tensor(state).unsqueeze(0).unsqueeze(0)  # Shape (1, 1, 4, 4)
        policy, value = model(state_tensor)

        # Sample action from policy
        dist = Categorical(policy)
        action = dist.sample()
        log_prob = dist.log_prob(action)

        # Perform action
        move = directions.get(action.item())
        env.update(move[0], move[1])
        reward = calculate_fitness(env.board)

        # Save transition
        states.append(state)
        actions.append(action.item())
        rewards.append(reward)
        dones.append(done)
        log_probs.append(log_prob.item())
        values.append(value.item())

        # Update state
        state = preprocess_board(env.board)
        env.check_game_state()
        done = not env.is_on()

    # Compute discounted rewards
    returns = []
    G = 0
    for reward, done in zip(reversed(rewards), reversed(dones)):
        G = reward + gamma * G * (1 - done)
        returns.insert(0, G)

    # Normalize returns
    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + 1e-8)

    # Update model using PPO objective
    states_tensor = torch.tensor(states).unsqueeze(1)  # Shape (batch, 1, 4, 4)
    actions_tensor = torch.tensor(actions)
    old_log_probs = torch.tensor(log_probs)
    values_tensor = torch.tensor(values)

    for _ in range(epochs):
        policy, value = model(states_tensor)
        dist = Categorical(policy)
        new_log_probs = dist.log_prob(actions_tensor)
        entropy = dist.entropy().mean()

        # PPO ratio
        ratio = torch.exp(new_log_probs - old_log_probs)

        # Surrogate objective
        advantages = returns - values_tensor
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1 - clip_eps, 1 + clip_eps) * advantages
        policy_loss = -torch.min(surr1, surr2).mean()

        # Value loss
        value_loss = F.mse_loss(value.squeeze(), returns)

        # Total loss
        loss = policy_loss + 0.5 * value_loss - 0.01 * entropy

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
