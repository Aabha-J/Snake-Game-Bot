from game_class import SnakeGame

import pygame

if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        # stop if game over
        if game_over == True:
            break

    print('Game Over')
    print('Final Score: ', score)


    pygame.quit()
    