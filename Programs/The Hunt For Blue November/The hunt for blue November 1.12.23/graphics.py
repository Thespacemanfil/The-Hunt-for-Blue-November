import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
BLUE = (0, 0, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

def draw_map():
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Draw Map")

def draw_player(map_scale, player):
    # Fill the screen with blue
    screen.fill(BLUE)

    # Calculate line endpoints based on player heading
    line_length = (10 + (2 * player.speed)) * map_scale  # Length of the line
    player_heading_rad = math.radians(player.heading)  # Convert heading to radians
    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # Starting point at screen center

    # Calculate the end coordinates of the line based on trigonometry
    x2 = x1 + line_length * math.sin(player_heading_rad)
    z2 = z1 - line_length * math.cos(player_heading_rad)

    # Draw a black dot at the center of the screen
    dot_size = 3
    pygame.draw.circle(screen, BLACK, (x1, z1), dot_size)

    # Draw a black line in the direction of player's heading
    pygame.draw.line(screen, BLACK, (x1, z1), (x2, z2), 2)

    # Update the display
    pygame.display.flip()

def draw_ship(map_scale, player, ship):
    # Calculate line endpoints based on enemy heading z1and position
    line_length = (3 * ship.speed * map_scale)  # Length of the line for the enemy
    ship_heading_rad = math.radians(ship.heading)  # Convert heading to radians

    # Calculate the end coordinates of the line based on enemy's position and direction
    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    x1 += int((player.x - ship.x) * map_scale)
    z1 += int((player.z - ship.z) * map_scale)
    x2 = x1 + line_length * math.sin(ship_heading_rad)
    z2 = z1 - line_length * math.cos(ship_heading_rad)

    # Draw a dot for the enemy at its position
    dot_size = 5
    pygame.draw.circle(screen, RED, (x1, z1), dot_size)

    # Draw the enemy line
    pygame.draw.line(screen, RED, (x1, z1), (x2, z2), 2)

    # Update the display
    pygame.display.flip()

def draw_torpedo(map_scale, player, torpedo):
    # Calculate line endpoints based on enemy heading z1and position
    line_length = (3 * torpedo.speed * map_scale)  # Length of the line for the enemy
    ship_heading_rad = math.radians(torpedo.heading)  # Convert heading to radians

    # Calculate the end coordinates of the line based on enemy's position and direction
    x1, z1 = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    x1 += int((player.x - torpedo.x) * map_scale)
    z1 += int((player.z - torpedo.z) * map_scale)
    x2 = x1 + line_length * math.sin(ship_heading_rad)
    z2 = z1 - line_length * math.cos(ship_heading_rad)

    # Draw a dot for the enemy at its position
    dot_size = 2
    pygame.draw.circle(screen, RED, (x1, z1), dot_size)

    # Draw the enemy line
    pygame.draw.line(screen, RED, (x1, z1), (x2, z2), 2)

    # Update the display
    pygame.display.flip()