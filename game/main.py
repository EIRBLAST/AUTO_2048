import pygame
from game_2048 import Game

def main():
    # Initialize the game
    pygame.init()
    game = Game(size=4,draw=True)
    game.add_new_tile()
    game.add_new_tile()

    # Game loop
    while game.is_on():
        print(game.is_on())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.end()
            if event.type == pygame.KEYUP:
                vector = [0, 0]
                if event.key == pygame.K_UP:
                    vector = [0, -1]
                elif event.key == pygame.K_DOWN:
                    vector = [0, 1]
                elif event.key == pygame.K_RIGHT:
                    vector = [1, 0]
                elif event.key == pygame.K_LEFT:
                    vector = [-1, 0]
                elif event.key == pygame.K_ESCAPE:
                    game.end()
                elif event.key == pygame.K_r:
                    game.reset()
                
                game.update(vector[0], vector[1])
        game.check_game_state()
        pygame.display.update()

if __name__ == "__main__":
    main()