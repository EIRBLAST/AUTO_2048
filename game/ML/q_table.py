"""
We now define here the Q_table from all the possible states
it's structure is like this
------------------------------------
        | Up | Down | Left | Right |
 State 1| Q1  |  Q2 ...............|
 State 2| .. . . ..................|
    .
    .
    .
    .
 State N|..........................|
"""

from ML.game_states import States

Q_table = {state.get_id():[0,0,0,0] for state in States}

if __name__ == "__main__":
    print(len(States))
    print(len(Q_table))
    import random
    r = random.choices(list(Q_table.keys()),k=10)
    print(r)
    import json
    with open("q_table.json", "w") as fp:
      json.dump(Q_table, fp) 