from ML.q_table import Q_table
from ML.game_states import State
from ML.eval_functions import monotonicity_value, find_highest_tile,calculate_fitness
from os.path import exists

from game_2048 import Game
import json
import random
import numpy as np

# Initialize all the Variable

# Use to convert the model choice to what the gmae understands
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

# If we already trained the model continue training
if exists("q_table.json"):
    with open("q_table.json","r") as fp:
        Q_table = json.loads(fp)

espsilon = 1 # Exploration probability
learning_rate = 0.1
discount_factor = 0.9

episodes = range(1)

for episode in episodes:
    curren_game = Game(draw=False)
    curren_game.add_new_tile()
    curren_game.add_new_tile()

    position,highest_tile = find_highest_tile(np.array(curren_game.board))
    empty_tiles  = np.size(np.array(curren_game.board)) - np.count_nonzero(np.array(curren_game.board))
    monotonicity = monotonicity_value(np.array(curren_game.board))
    highest_tile_side = location.get(position)
    current_state = State(highest_tile,monotonicity,empty_tiles,highest_tile_side)
    print(highest_tile,monotonicity,empty_tiles,highest_tile_side)
    while curren_game.is_on():

        # Choose a random action based on the Exploration value
        if random.uniform(0,1) < espsilon:
            action = random.randint(0,3)
            move = directions.get(action)
        else:
            actions = Q_table.get(current_state.get_id())
            action = actions.index(max(actions))
            move = direction.get(action)
        
        # Perfom the actions
        curren_game.update(move[0], move[1])
        reward = calculate_fitness(curren_game)
        

        # We get the current state of the game
        position,highest_tile = find_highest_tile(np.array(curren_game.board))
        empty_tiles  = np.size(np.array(curren_game.board)) - np.count_nonzero(np.array(curren_game.board))
        monotonicity = monotonicity_value(np.array(curren_game.board))
        highest_tile_side = location.get(position)
        new_state = State(highest_tile,monotonicity,empty_tiles,highest_tile_side)

        # Update the Q table
        actions = Q_table.get(new_state.get_id())
        best_future_q = max(actions)
        Q_table[current_state.get_id()][action] = Q_table[current_state.get_id()][action] + learning_rate * (reward + discount_factor * best_future_q - Q_table[current_state.get_id()][action])
        
        current_state = new_state
        curren_game.check_game_state()
    espsilon *= 0.75

# Save the result and use them later

with open("q_table.json", "w") as fp:
    json.dump(Q_table, fp) 