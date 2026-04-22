import pygame
import math
from constants import *

'''Effects Module: Handles all visual gameplay overlays:
- Aim direction 
- Projectile trajectory preview 
- Power bar UI 
- Wind indicator'''


# aiming arrow
def draw_aim(surface, game):
    
    # draws the aiming arrow showing shot direction
    ox, oy = game._current().aim_origin()

    length = 50
    ex = ox + math.cos(game.aim_angle) * length
    ey = oy + math.sin(game.aim_angle) * length

    # main aim line
    pygame.draw.line(surface, DARK_GRAY, (ox, oy), (int(ex), int(ey)), 2)

    # arrowhead - two small angled lines
    for offset in [2.7, -2.7]:
        a = game.aim_angle + offset
        pygame.draw.line(surface, DARK_GRAY,
            (int(ex), int(ey)),
            (int(ex + 10 * math.cos(a)), int(ey + 10 * math.sin(a))), 2)


# trajectory preview 
def draw_trajectory_preview(surface, game):
    
    # draws predicted projectile path based on physics simulation 
    ox, oy = game._current().aim_origin()

    # intial velocity based on aim and power 
    vx = math.cos(game.aim_angle) * game.power * VELOCITY_SCALE
    vy = math.sin(game.aim_angle) * game.power * VELOCITY_SCALE

    px, py = float(ox), float(oy)

    # simulates projectile motion 
    for i in range(60):
        
        # wind and gravity effects
        vx += game.wind * WIND_FACTOR
        vy += GRAVITY
        
        # updates position 
        px += vx
        py += vy

        # draws small dotted trail 
        if i % 3 == 0:
            pygame.draw.circle(surface, GRAY, (int(px), int(py)), 2)

        # stops if projectile hits the ground 
        if py > GROUND_Y:
            break


# power bar UI
def draw_power_bar(surface, game, font_small):

    # draws the power/charge bar anchored to the heal button UI 
    player = game._current()

    # anchor to heal button instead of player body
    heal_rect = player.get_heal_rect()

    x = heal_rect.x
    y = heal_rect.y - 20   # position above heal button

    w = heal_rect.width
    h = 14

    # background box 
    pygame.draw.rect(surface, (230, 230, 230),
                     (x - 4, y - 22, w + 8, h + 26),
                     border_radius=6)
    pygame.draw.rect(surface, BLACK,
                     (x - 4, y - 22, w + 8, h + 26),
                     1, border_radius=6)

    # bar outline
    pygame.draw.rect(surface, BLACK, (x, y, w, h), 2)

    # fill based on current power 
    fill = int(w * (game.power / MAX_POWER))
    if fill > 0:
        pygame.draw.rect(surface, BLACK, (x + 2, y + 2, fill - 4, h - 4))

    # label text 
    label = font_small.render("POWER", True, BLACK)
    surface.blit(label, (x, y - 18))


# wind indicator 
def draw_wind(surface, game, font_small):

    # draws wind direction and strength indicator 
    cx, cy = WIDTH // 2, 100

    # label 
    label = font_small.render("WIND", True, BLACK)
    surface.blit(label, (cx - label.get_width() // 2, cy - 20))

    arrow_len = abs(game.wind) * 30

    # no wind case
    if game.wind == 0:
        pygame.draw.circle(surface, BLACK, (cx, cy + 5), 3)
        
        # wind direction arrow 
    else:
        end_x = int(cx + (arrow_len if game.wind > 0 else -arrow_len))
        pygame.draw.line(surface, BLACK, (cx, cy + 5), (end_x, cy + 5), 2)

        # arrowhead direction 
        d = 1 if game.wind > 0 else -1
        pygame.draw.polygon(surface, BLACK, [
            (end_x, cy + 5), (end_x - d * 8, cy), (end_x - d * 8, cy + 10)
        ])

    # numeric wind value 
    value = font_small.render(f"{abs(game.wind):.1f}", True, BLACK)
    surface.blit(value, (cx - value.get_width() // 2, cy + 14))