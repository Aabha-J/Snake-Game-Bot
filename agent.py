import torch
import random
import numpy as np
from collections import deque
from ai_game_class import SnakeGame_forAI
from game_class import Direction, Point, BLOCK_SIZE


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # controls exploration/randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #Remove elements from left if u exceed size
        # self.model = Linear_QNet(11, 256, 3)
        # self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]

        point_left = Point(head.x - BLOCK_SIZE, head.y)
        point_right = Point(head.x + BLOCK_SIZE, head.y)
        point_up = Point(head.x, head.y - BLOCK_SIZE)
        point_down = Point(head.x,head.y + BLOCK_SIZE )

        dir_left = game.direction == Direction.LEFT
        dir_right = game.direction == Direction.RIGHT
        dir_up = game.direction == Direction.UP
        dir_down = game.direction = Direction.DOWN

        state = [

            # Danger straight
            (dir_right and game.is_collided(point_right)) or
            (dir_left and game.is_collided(point_left)) or
            (dir_up and game.is_collided(point_up)) or
            (dir_down and game.is_collided(point_down))


        ]

    def remember(self, state, action, reward, next_state, game_over):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, game_over):
        pass

    def get_action(self, state):
        pass


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGame_forAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #train short memroy
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        #remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                # agent.model.save()
            print('Game Number: ', agent.n_games, 'Score: ', score, 'Record: ', record)

            # plot_scores

    

if __name__ == '__main__':
    train()