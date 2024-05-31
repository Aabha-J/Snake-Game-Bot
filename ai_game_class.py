import pygame
from game_class import SnakeGame, Direction, Point, BLOCK_SIZE, SPEED
import numpy as np

class SnakeGame_forAI(SnakeGame):
    def __init__(self, w=640, h=480):
        self.frame_count = 0
        super().__init__(w, h)  # Call the parent class constructor
        self.reset()
        

    def reset(self):
        # Call the parent class reset method
        super().reset()
        self.frame_count = 0

    def play_step(self, action):
        self.frame_count += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.snake_head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collided() or self.frame_count > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.snake_head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self.update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.snake_head.x
        y = self.snake_head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.snake_head = Point(x, y)
