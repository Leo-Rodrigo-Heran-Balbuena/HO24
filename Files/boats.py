import pygame
import random


screen = pygame.display.set_mode(600,600)

boat_list = list()
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
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

def random_border_position(): #get random position on the border
    side = random.randint(1, 4)  # 1=Top, 2=Right, 3=Bottom, 4=Left
    if side == 1:  # Top
        return random.randint(0, SCREEN_WIDTH), 0
    elif side == 2:  # Right
        return SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)
    elif side == 3:  # Bottom
        return random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT
    else:  # Left
        return 0, random.randint(0, SCREEN_HEIGHT)

def gen_boats(number_of_boats):
    for _ in range(number_of_boats):
        position = random_border_position()
        boat = pygame.Rect(position[0], position[1], 20, 20)
        direction = random.choice([UP, DOWN, LEFT, RIGHT, DIAGONAL])  # Random direction
        speed = 10  # Fixed speed, can be randomized as well
        boat_list.append((boat, direction, speed))


def move_boats(speed):
    for boat in boat_list[:]:
        boat[BOAT_RECT].move_ip(boat[BOAT_DIRECTION][X] * boat[BOAT_SPEED], boat[BOAT_DIRECTION][Y] * boat[BOAT_SPEED])
    if boat[BOAT_RECT].right < 0 or boat[BOAT_RECT].left > SCREEN_WIDTH or boat[BOAT_RECT].bottom < 0 or boat[BOAT_RECT].top > SCREEN_HEIGHT:
            boat_list.remove(boat)
