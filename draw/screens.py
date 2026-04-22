import pygame
from constants import *

from draw.characters import draw_character
from draw.environment import draw_fence

''' Screen module - Handles full-screen UI states:
- Title screen 
- Game over screen '''

# title screen 
def draw_title(surface, game, renderer):
    
    # game title 
    title = renderer.font_large.render("Animal Tower", True, BLACK)
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    
    # character showcase layout 
    spacing = 140
    center_x = WIDTH // 2
    y = 320

    positions = [
        center_x - (1.5 * spacing),
        center_x - (0.5 * spacing),
        center_x + (0.5 * spacing),
        center_x + (1.5 * spacing),
    ]

    names = ["Cat", "Dog", "Wolf", "Elephant"]

    # draws each character preview 
    for x, name in zip(positions, names):
        draw_character(surface, int(x), y, name, renderer.font_small)

    # game mode options 
    opt1 = renderer.font_medium.render("Press [1] - 1 Player (vs AI)", True, BLACK)
    surface.blit(opt1, (WIDTH // 2 - opt1.get_width() // 2, 410))
    
    opt2 = renderer.font_medium.render("Press [2] - 2 Players", True, BLACK)
    surface.blit(opt2, (WIDTH // 2 - opt2.get_width() // 2, 450))

# game over screen 
def draw_game_over(surface, game, renderer):
    # draws the game over overlay with winner and restart options 
    
    # semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((235, 235, 235, 200))
    surface.blit(overlay, (0, 0))

    # winner text
    text = renderer.font_large.render(f"{game.winner} Wins!", True, BLACK)
    surface.blit(
        text,
        (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60)
    )

    # restart instruction
    restart_text = renderer.font_medium.render("Press [R] to Restart", True, BLACK)
    surface.blit(
        restart_text,
        (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10)
    )

    # mode selection instruction 
    menu_text = renderer.font_small.render(
        "Press [1] - 1 Player (vs AI) or Press [2] - 2 Players", 
        True, 
        BLACK
    )
    surface.blit(
        menu_text,
        (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 + 40)
    )