import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()

font = pygame.font.SysFont('sans', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

BLOCK_SIZE = 20
SPEED = 15

#RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

Point = namedtuple('Point', 'x, y')

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.window_width = w
        self.window_height = h

        # display

        #display
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Snake")

        #Clock to control speed
        self.clock = pygame.time.Clock()

        # Initilize game state
        self.direction = Direction.RIGHT


        self.snake_head = Point(self.window_width//2, self.window_height//2)
        self.snake = [self.snake_head, 
                      Point(self.snake_head.x - BLOCK_SIZE, self.snake_head.y),
                      Point(self.snake_head.x - 2*BLOCK_SIZE, self.snake_head.y)]
        self.score = 0
        self.food = None

        self.place_food()

        #game state

    def place_food(self):
        x = random.randint(0, (self.window_width - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.window_height - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()



    def play_step(self):
        #1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:  #if the user presses a key
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        #2. move
        self.move_snake(self.direction)
        self.snake.insert(0, self.snake_head)
        

        #3 . check if game over
        game_over = False
        if self.is_collided():
            game_over = True
            return game_over, self.score
        

        #4. new food
        if self.snake_head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

        # 5 . update ui and clock
        self.update_ui()
        self.clock.tick(SPEED)

        self.update_ui()
        self.clock.tick(SPEED)

        #7. Return game over and player's score
        game_over = False
        return game_over, self.score

    def update_ui(self):
        self.window.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.window, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.window, BLUE2, pygame.Rect(pt.x+4, pt.y+4, BLOCK_SIZE//2, BLOCK_SIZE//2))

        pygame.draw.rect(self.window, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.window.blit(text, [0, 0])
        pygame.display.flip() #Update display

    def move_snake(self, direction):
        x = self.snake_head.x
        y = self.snake_head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.snake_head = Point(x, y)

    def is_collided(self):
        if self.snake_head.x > self.window_width - BLOCK_SIZE or self.snake_head.x < 0 or self.snake_head.y > self.window_height - BLOCK_SIZE or self.snake_head.y < 0:
            return True
        if self.snake_head in self.snake[1:]:
            return True
        return False