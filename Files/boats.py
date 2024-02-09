import pygame
import random

boat_list = list()

# INDEXING
X, Y = 0, 1
BOAT_RECT, BOAT_DIRECTION, BOAT_SPEED = 0, 1, 2

# COLORS
RED = (255, 0, 0, 0)

# DIRECTIONS
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIAGONAL = (1, 1)

# CHARACTER PROPERTIES
speed = 10


def gen_boats(number_of_boats):
    for i in range(0, number_of_boats):
        number_of_boats.append((pygame.Rect(random(0, 2), random(0, 5), 20, 20), DIAGONAL, (0, 2)))


def move_boats(speed):
    for boat in boat_list:
        boat[BOAT_RECT].move(DIAGONAL[X] * speed, DIAGONAL[Y] * speed)
