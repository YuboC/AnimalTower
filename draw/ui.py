import pygame
from constants import *

''' UI module - Handles all player interface elements:
- Health bars 
- Buttons (heal, special, shield)
- XP and level UI 
- Defensive visuals '''

# health bar 
def draw_health_bar(surface, x, y, hp, max_hp, name, font_small, font_log):
    # draws player health bar with name and attack label
    
    w, h = 180, 18

    # outline
    pygame.draw.rect(surface, BLACK, (x, y, w, h), 2)

    # fill ratio
    ratio = hp / max(1, max_hp)
    fill_w = int(w * ratio)

    # filled portion 
    if fill_w > 0:
        pygame.draw.rect(surface, DARK_GRAY, (x + 2, y + 2, fill_w - 4, h - 4))

    # player name and HP text 
    label = font_small.render(f"{name}: {hp}/{max_hp}", True, BLACK)
    surface.blit(label, (x + 5, y + h + 4))

    # attack label - placeholder / UI indicator 
    atk_text = font_log.render("Atk", True, DARK_GRAY)
    surface.blit(atk_text, (x + 5, y + h + 20))



# heal button 
def draw_heal_button(surface, player, font_btn):
    # draws the heal button - only active when XP bar is full
    
    mx, my = pygame.mouse.get_pos()


    btn_rect = pygame.Rect(UI_HEAL_X, UI_BAR_Y, UI_BUTTON_W, UI_BUTTON_H)
    hovering = btn_rect.collidepoint(mx, my)

    # determines color based on state 
    if not player.can_heal():
        color = (120, 120, 120)
    else:
        color = (90, 200, 110) if hovering else (70, 170, 90)

    # shadow 
    pygame.draw.rect(surface, (0, 0, 0, 60), btn_rect.move(2, 2), border_radius=6)
    
    # button 
    pygame.draw.rect(surface, color, btn_rect, border_radius=6)
    pygame.draw.rect(surface, BLACK, btn_rect, 2, border_radius=6)

    # label text 
    if player.can_heal():
        label = "HEAL"
    elif player.exp < XP_HEAL_COST:
        label = "NO XP"
    else:
        label = "FULL HP"
    txt = font_btn.render(label, True, WHITE)

    surface.blit(
        txt, 
        (
            btn_rect.x + btn_rect.w // 2 - txt.get_width() // 2,
            btn_rect.y + btn_rect.h // 2 - txt.get_height() // 2
        )
    )

    return btn_rect


# special button 
def draw_special_button(surface, player, font_btn):
    # draws the special ability button with cooldown and usage states
    mx, my = pygame.mouse.get_pos()

    btn_rect = pygame.Rect(UI_SPECIAL_X, UI_BAR_Y, UI_BUTTON_W, UI_BUTTON_H)
    hovering = btn_rect.collidepoint(mx, my)

    # state logic 
    
    # fully used 
    if player.special_used >= player.max_specials:
        color = (80, 80, 80)
        label = "USED"

    # cooldown active 
    elif player.special_cooldown > 0:
        color = (150, 80, 200)
        label = "CD"

    # ready to use 
    else:
        color = (180, 100, 230) if hovering else (150, 80, 200)
        label = "SPECIAL"
    
    # shadow
    pygame.draw.rect(surface, (0, 0, 0, 60), btn_rect.move(2, 2), border_radius=6)
    
    # button  
    pygame.draw.rect(surface, color, btn_rect, border_radius=6)
    pygame.draw.rect(surface, BLACK, btn_rect, 2, border_radius=6)

    # text 
    txt = font_btn.render(label, True, WHITE)

    surface.blit(
        txt, 
        (
            btn_rect.x + btn_rect.w // 2 - txt.get_width() // 2,
            btn_rect.y + btn_rect.h // 2 - txt.get_height() // 2
            )
    )

    return btn_rect


# shield button
def draw_shield_button(surface, player, font_btn):
    # draws shield button with hover and used states 
    mx, my = pygame.mouse.get_pos()

    btn_rect = pygame.Rect(UI_SHIELD_X, UI_BAR_Y, UI_BUTTON_W, UI_BUTTON_H)
    hovering = btn_rect.collidepoint(mx, my)

    if player.shield_used:
        color = (100, 100, 100)
    else:
        color = (80, 160, 255) if hovering else (60, 140, 230)

    # shadow 
    pygame.draw.rect(surface, (0, 0, 0, 60), btn_rect.move(2, 2), border_radius=6)
    
    # button 
    pygame.draw.rect(surface, color, btn_rect, border_radius=6)
    pygame.draw.rect(surface, BLACK, btn_rect, 2, border_radius=6)

    # label 
    label = "SHIELD" if not player.shield_used else "USED"
    txt = font_btn.render(label, True, WHITE)

    surface.blit(
        txt, 
        (
            btn_rect.x + btn_rect.w // 2 - txt.get_width() // 2,
            btn_rect.y + btn_rect.h // 2 - txt.get_height() // 2
        )
    )

    return btn_rect


# defensive visuals
def draw_defend_bubble(surface, x, y):
    # draws a semi-transparent shield bubble around a player
    
    radius = 45
    bubble = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    pygame.draw.circle(bubble, (255, 255, 255, 70), (radius, radius), radius)
    pygame.draw.circle(bubble, (200, 200, 255, 120), (radius, radius), radius, 2)

    surface.blit(bubble, (x - radius, y - radius - 5))
     
    
# XP bar
def draw_xp_bar(surface, x, y, xp, font_small):
    # draws XP bar - fills up toward heal cost
    
    w, h = 180, 10

    ratio = min(xp / max(1, XP_HEAL_COST), 1)

    # background
    pygame.draw.rect(surface, (40, 40, 40), (x, y, w, h))
    pygame.draw.rect(surface, BLACK, (x, y, w, h), 2)

    # fill - green when full, blue when charging
    fill_w = int(w * ratio)
    color = (80, 200, 100) if ratio >= 1.0 else (80, 180, 255)
    pygame.draw.rect(surface, color, (x + 1, y + 1, fill_w - 2, h - 2))

    # text
    if ratio >= 1.0:
        txt = font_small.render(f"XP: HEAL READY", True, BLACK)
    else:
        txt = font_small.render(f"XP: {xp}/{XP_HEAL_COST}", True, BLACK)
    surface.blit(txt, (x, y + 12))
        

#player turn and damage UI
def draw_player_ui(surface, font_small, font_medium, x, name, dmg, bar_y, is_active):
    # displays current turn and estimated damage for a player 
    
    # active turn indicator
    if is_active:
        turn_text = font_medium.render(f"{name}'s Turn", True, BLACK)
        surface.blit(turn_text, (x, 20))

    # damage preview 
    dmg_text = font_small.render(f"Damage: {dmg}", True, (255, 0, 0))
    surface.blit(dmg_text, (x, bar_y - 35))