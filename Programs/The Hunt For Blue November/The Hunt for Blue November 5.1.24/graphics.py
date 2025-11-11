import pygame as pg
import math
import numpy as np

# Initialize Pygame
pg.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 800
BLUE = (25,45,187)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GRAY = (55, 55, 55)

def draw_map():
    global screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Draw Map")

def draw_background():
    # Fill the screen with blue
    screen.fill(BLUE)

def draw_player(map_scale, player):
    # Calculate line endpoints based on player heading
    line_length = (10 + (2 * player.tgt_speed)) * map_scale  # Length of the line
    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Starting point at screen center

    # Calculate the end coordinates of the line based on trigonometry
    x2 = x1 + line_length * math.sin(player.tgt_heading)
    z2 = z1 - line_length * math.cos(player.tgt_heading)

    # Draw a white line in the direction of player's tgt heading
    pg.draw.line(screen, WHITE, (x1, z1), (x2, z2), 1)

    # Calculate line endpoints based on player heading
    line_length = (10 + (2 * player.speed)) * map_scale  # Length of the line
    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Starting point at screen center

    # Calculate the end coordinates of the line based on trigonometry
    x2 = x1 + line_length * math.sin(player.heading)
    z2 = z1 - line_length * math.cos(player.heading)

    # Draw a black line in the direction of player's heading
    pg.draw.line(screen, BLACK, (x1, z1), (x2, z2), 2)

    # Draw a black dot at the center of the screen
    dot_size = 50 * map_scale
    pg.draw.circle(screen, BLACK, (x1, z1), dot_size)

def draw_ship(map_scale, enemies, player, ship):
    x1, z1, x2, z2 = relative(map_scale, player, ship)

    # Draw a dot for the enemy at its position
    dot_size = 40 * map_scale
    pg.draw.circle(screen, RED, (x1, z1), dot_size)

    # Draw the enemy line
    pg.draw.line(screen, RED, (x1, z1), (x2, z2), 2)

    try:
        if ship == enemies[player.target]:
            square_size = 200 * map_scale  # Adjust this value as needed
            # Calculate the rectangle position and size
            square_rect = pg.Rect(x1 - square_size // 2, z1 - square_size // 2, square_size, square_size)
            # Draw the square
            pg.draw.rect(screen, BLACK, square_rect, 2)
    except: pass

def draw_torpedo(map_scale, player, torpedo):
    x1, z1, x2, z2 = relative(map_scale, player, torpedo)

    # Draw a dot for the torpedo at its position
    dot_size = 20 * map_scale
    pg.draw.circle(screen, GRAY, (x1, z1), dot_size)

    # Draw the torpedo line
    pg.draw.line(screen, GRAY, (x1, z1), (x2, z2), 2)

def relative(map_scale, player, object):
    line_length = (3 * object.speed * map_scale)

    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    x1 += int((object.x - player.x) * map_scale)
    z1 -= int((object.z - player.z) * map_scale)
    x2 = x1 + line_length * math.sin(object.heading)
    z2 = z1 - line_length * math.cos(object.heading)

    return x1, z1, x2, z2

def draw_ui(map_scale):
    GAME_FONT = pg.freetype.Font("red october.ttf", 20)
    x1, z1 = SCREEN_WIDTH // 50, SCREEN_HEIGHT // 20  # Starting point at screen corner
    multiplier = int(np.round(0.1/map_scale) + 1)
      
    z2 = z1 + (1000 * map_scale * multiplier)
    text = str(multiplier) + "km"
    GAME_FONT.render_to(screen, ((x1 - 20), (z1 - 30)), text, BLACK)
    pg.draw.line(screen, BLACK, (x1, z1), (x1, z2), 3)

    pg.display.flip()

def pause():
    x1, z1 = SCREEN_WIDTH // 2.1, SCREEN_HEIGHT // 2
    GAME_FONT = pg.freetype.Font("red october.ttf", 50)
    GAME_FONT.render_to(screen, (x1, z1), "PAUSED", BLACK)
    pg.display.flip()


def win():
    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    screen.fill(BLACK)
    GAME_FONT = pg.freetype.Font("red october.ttf", 50)
    GAME_FONT.render_to(screen, (x1 - 50, z1), "YOU WIN", RED)
    pg.display.flip()

def gameover():
    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    screen.fill(BLACK)
    GAME_FONT = pg.freetype.Font("red october.ttf", 50)
    GAME_FONT.render_to(screen, (x1 - 50, z1), "YOU SINK", RED)
    pg.display.flip()