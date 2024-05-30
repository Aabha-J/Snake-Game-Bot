import pygame
import random
from enum import Enum
from collections import namedtuple
from game_class import SnakeGame, Direction, Point, WHITE, RED, BLUE1, BLUE2, BLACK

class SnakeGame_forAI(SnakeGame):
    def __init__(self, w=640, h=480):
        super().__init__(w, h)  # Call the parent class constructor
        # Additional modifications or customizations here
        self.frame_count = 0

    def reset(self):
        # Call the parent class reset method
        super().reset()
        self.frame_count = 0

    def move_snake(self, direction):
        # Call the corresponding method from SnakeGame
        super().move_snake(direction)

       

    def play_step(self):
        # use the parent class method for now
        game_over, score = super().play_step()
        return game_over, score
