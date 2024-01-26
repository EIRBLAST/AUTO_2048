"""
State definition
#-------------------------------------#

State : 
Highest Tile | Monotonicity | empty tiles | highest tile side
 11 states      256 states      10 states     4 states

100k * 4 board (Big but manageable)

We then create this aformentioned state list
"""

class State:
    def __init__(self,highest_tile,monotonicity,empty_tiles,highest_tile_side):
        self.highest_tile = highest_tile
        self.empty_tiles = empty_tiles
        self.monotonicity = monotonicity
        self.hight_tile_side = highest_tile_side 

    def get_id(self):
        return f"{self.highest_tile}-{self.monotonicity}-{self.empty_tiles}-{self.hight_tile_side}"

States:list[State] = []
for highest_tile_i in range(0,12):
    for empty_tiles_i in range(17):
        for monotonicity_i in range(257):
            for hight_tile_side_i in range(4):
                States.append(State(2**highest_tile_i,monotonicity_i,empty_tiles_i,hight_tile_side_i))

if __name__ == "__main__":
    print(len(States))
"""
We now have a list of all possible states
"""