import pygame
from constants import *

''' Environemnt Rendering: 
Handles static world elements: 
- Ground 
- Fence obstacle '''

# ground 
def draw_ground(surface):

    # draws the ground line across the screen 
    pygame.draw.line(surface, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)


# fence 
def draw_fence(surface, x, ground_y):
    # draws a stylized fence obstacle at a given x position 
    # calculates top of fence based on height 
    top = ground_y - FENCE_HEIGHT


    # vertical posts 
    for dx in [-15, 0, 15]:
        pygame.draw.line(surface, DARK_GRAY, (x + dx, ground_y), (x + dx, top), 3)

    # horizontal rails 
    pygame.draw.line(surface, DARK_GRAY, (x - 22, top + 25), (x + 22, top + 25), 2)
    pygame.draw.line(surface, DARK_GRAY, (x - 22, top + 60), (x + 22, top + 60), 2)

    # decorative pointed tops 
    for dx in [-15, 0, 15]:
        pts = [(x + dx - 4, top), (x + dx, top - 10), (x + dx + 4, top)]
        pygame.draw.polygon(surface, DARK_GRAY, pts, 2)