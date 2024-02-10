from TSPDecoder import *
import pygame
import random

rows, columns = 27, 19
TSP = TSPDecoder(rows=rows, columns=columns)

# Define constants
PIXEL_WIDTH = 20
PIXEL_HEIGHT = 10
PIXEL_MARGIN = 2
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Corrected color tuple
SCREEN_WIDTH = columns * PIXEL_WIDTH + columns * PIXEL_MARGIN + 2 * PIXEL_MARGIN
SCREEN_HEIGHT = rows * PIXEL_HEIGHT + rows * PIXEL_MARGIN + 2 * PIXEL_MARGIN
last_spawn_time = 0  # Tracks when the last boat was spawned
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
TARGET_SIZE = 50  # Size of the target area (square side length)
target_area = pygame.Rect(SCREEN_CENTER[0] - TARGET_SIZE // 2, SCREEN_CENTER[1] - TARGET_SIZE // 2, TARGET_SIZE,
                          TARGET_SIZE)

# INDEXING
X, Y = 0, 1
BOAT_RECT, BOAT_DIRECTION, BOAT_SPEED = 0, 1, 2

# DIRECTIONS
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIAGONAL = (1, 1)

# CHARACTER PROPERTIES
speed = 2

boat_list = []

# Initialise the PyGame screen according to resolution
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Game Signoff")

pygame.font.init()  # Initialize the font module
font = pygame.font.SysFont(None, 36)  # Create a font object with default font and size 36
total_boats_reached_center = 0  # Initialize this before the game loop

# Initialise the PyGame Clock for timing
clock = pygame.time.Clock()


def check_boats_center():
    global boat_list
    boats_reached_center = 0
    for boat in boat_list[:]:
        if target_area.contains(boat[BOAT_RECT]):
            boat_list.remove(boat)  # Optional: Remove boat after reaching the center
            boats_reached_center += 1
    return boats_reached_center


def random_border_position():
    side = random.randint(1, 4)
    if side == 1:  # Top
        return random.randint(0, SCREEN_WIDTH), 0
    elif side == 2:  # Right
        return SCREEN_WIDTH - 20, random.randint(0, SCREEN_HEIGHT)
    elif side == 3:  # Bottom
        return random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT - 20
    else:  # Left
        return 0, random.randint(0, SCREEN_HEIGHT)


def gen_boats(number_of_boats):
    global boat_list
    for _ in range(number_of_boats):
        position = random_border_position()
        boat = pygame.Rect(position[0], position[1], 20, 20)
        direction = random.choice([UP, DOWN, LEFT, RIGHT, DIAGONAL])
        boat_list.append([boat, direction, speed])


def move_boats():
    global boat_list
    for boat in boat_list[:]:
        # Determine direction based on position relative to screen center
        direction_x = 1 if boat[BOAT_RECT].centerx < SCREEN_CENTER[0] else -1
        direction_y = 1 if boat[BOAT_RECT].centery < SCREEN_CENTER[1] else -1

        # Modify the boat's direction to head towards the center
        # This is a simplified approach; you might want to refine it based on your game's needs
        new_direction = (direction_x, direction_y)

        # Move the boat in the new direction
        boat[BOAT_RECT].move_ip(new_direction[X] * boat[BOAT_SPEED], new_direction[Y] * boat[BOAT_SPEED])

        # Check if the boat is out of screen bounds and remove it
        if boat[BOAT_RECT].right < 0 or boat[BOAT_RECT].left > SCREEN_WIDTH or boat[BOAT_RECT].bottom < 0 or boat[
            BOAT_RECT].top > SCREEN_HEIGHT:
            boat_list.remove(boat)


def remove_boat_on_touch(touch_pos):
    for index, boat in enumerate(boat_list):
        if boat[BOAT_RECT].collidepoint(touch_pos):
            del boat_list[index]  # Remove the boat if touch collides
            break  # Assume only one touch at a time


last_spawn_time = pygame.time.get_ticks()  # Initialize the spawn timer

while TSP.available():
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= 1000:  # Check if 1 second has elapsed
        gen_boats(1)  # Spawn one boat
        last_spawn_time = current_time  # Reset the timer
    # Check if the screen is closed and quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Get the frame
    grid = TSP.readFrame()

    move_boats()  # Move boats

    # Clear the screen by blacking it out
    screen.fill(BLACK)

    # Display the counter

    touch_pos = TSP.getTouch()  # Get touch coordinates
    if touch_pos is not None:
        remove_boat_on_touch(touch_pos)  # Handle touch event, assuming you adapt the function to accept touch_pos
    touch_pos = TSP.getTouch()


    rect_list = list()
    # Loop through all pixels in the frame
    for row in range(rows):
        for column in range(columns):
            # Get the pixel value and set the gray value accordingly
            pixel = grid[row][column]
            if grid[row][column] > 150:

                color = (pixel, pixel, pixel)

                rect_list.append(pygame.Rect(
                        PIXEL_MARGIN + ((PIXEL_MARGIN + PIXEL_WIDTH) * column),
                        PIXEL_MARGIN + ((PIXEL_MARGIN + PIXEL_HEIGHT) * row),
                        PIXEL_WIDTH,
                        PIXEL_HEIGHT))

    # Draw rectangles in the screen
    for i in rect_list:
        pygame.draw.rect(screen, color, i)
        boat_list_copy = boat_list.copy()
        for j in boat_list_copy:
            if (i.colliderect(j[BOAT_RECT])):
                boat_list.remove(j)
    # Draw boats
    for boat in boat_list:
        pygame.draw.rect(screen, RED, boat[BOAT_RECT])

    total_boats_reached_center += check_boats_center()
    counter_text = font.render(f"Boats Reached Center: {total_boats_reached_center}", True, (255, 255, 255))
    screen.blit(counter_text, (10, 10))
    # Limit the framerate to 60FPS
    clock.tick(60)

    # Draw to the display
    pygame.display.flip()
