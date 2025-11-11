import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 800
BLUE = (0, 0, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_map():
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Draw Map")

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
    pygame.draw.line(screen, WHITE, (x1, z1), (x2, z2), 1)


    # Calculate line endpoints based on player heading
    line_length = (10 + (2 * player.speed)) * map_scale  # Length of the line
    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Starting point at screen center

    # Calculate the end coordinates of the line based on trigonometry
    x2 = x1 + line_length * math.sin(player.heading)
    z2 = z1 - line_length * math.cos(player.heading)

    # Draw a black line in the direction of player's heading
    pygame.draw.line(screen, BLACK, (x1, z1), (x2, z2), 2)

    # Draw a black dot at the center of the screen
    dot_size = 50 * map_scale
    pygame.draw.circle(screen, BLACK, (x1, z1), dot_size)

    # Update the display
    #pygame.display.flip()

def draw_ship(map_scale, player, ship):
    x1, z1, x2, z2 = relative(map_scale, player, ship)

    # Draw a dot for the enemy at its position
    dot_size = 40 * map_scale
    pygame.draw.circle(screen, RED, (x1, z1), dot_size)

    # Draw the enemy line
    pygame.draw.line(screen, RED, (x1, z1), (x2, z2), 2)

    # Update the display
    #pygame.display.flip()

def draw_torpedo(map_scale, player, torpedo):
    x1, z1, x2, z2 = relative(map_scale, player, torpedo)

    # Draw a dot for the torpedo at its position
    dot_size = 20 * map_scale
    pygame.draw.circle(screen, RED, (x1, z1), dot_size)

    # Draw the torpedo line
    pygame.draw.line(screen, RED, (x1, z1), (x2, z2), 2)

    # Update the display
    #pygame.display.flip()

def relative(map_scale, player, object):
    line_length = (3 * object.speed * map_scale)

    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    x1 += int((object.x - player.x) * map_scale)
    z1 -= int((object.z - player.z) * map_scale)
    x2 = x1 + line_length * math.sin(object.heading)
    z2 = z1 - line_length * math.cos(object.heading)

    return x1, z1, x2, z2

def draw_ui(map_scale):
    GAME_FONT = pygame.freetype.Font("red october.ttf", 20)
    x1, z1 = SCREEN_WIDTH // 50, SCREEN_HEIGHT // 20  # Starting point at screen corner
    z2 = z1 + (1000 * map_scale)
    GAME_FONT.render_to(screen, ((x1 - 20), (z1 - 30)), "1 km", (0, 0, 0))
    pygame.draw.line(screen, BLACK, (x1, z1), (x1, z2), 3)

    pygame.display.flip()

def draw_selection(map_scale, player, ship):
    pygame.draw.rect(screen, BLACK, (100,-100,200,-200), 1)