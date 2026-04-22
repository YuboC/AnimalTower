import math
import pygame

''' Aiming logic - Handles player aiming based 
on mouse position. 

Responsibilities: 
- Computes aim direction from player to mouse 
- Clamps anle depending on current turn/plaer side 
- Prevents aim changes while projectile is active '''


# updates the current player's aim angle based on mouse position 
def update_aim(game):
    ''' Rules: 
    - Aim is locked while projectile is in flight 
    - Player 1 and 2 have different angle constraints '''

    # block aim while projectile is active 
    if game.projectile and game.projectile.alive:
        return

    # mouse position 
    mx, my = pygame.mouse.get_pos()
    
    # origin point of current player's aim
    ox, oy = game._current().aim_origin()

    # direction vector to mouse 
    dx = mx - ox
    dy = my - oy

    # raw angle toward mouse 
    angle = math.atan2(dy, dx)

    # player 1 (left side)
    if game.turn == 0:
        game.aim_angle = max(
            -math.pi / 2 - 0.3, 
            min(-0.05, angle)
        )
        
    # player 2 (right side)
    else:
        game.aim_angle = max(
            -math.pi + 0.05, 
            min(-math.pi / 2 + 0.3, angle)
        )