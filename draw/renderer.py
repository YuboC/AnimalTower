# drawing modules 
from draw.characters import draw_character
from draw.environment import draw_ground, draw_fence
from draw.effects import draw_aim, draw_wind
from draw.ui import (
    draw_health_bar,
    draw_heal_button,
    draw_defend_bubble,
    draw_special_button,
    draw_xp_bar,
    draw_shield_button,
    draw_player_ui 
)

from constants import PLAYER1_X, PLAYER1_Y, PLAYER2_X, PLAYER2_Y
from draw.log_panel import draw_history_log
from draw.screens import draw_title, draw_game_over
from draw.wind_effect import WindEffect

# game logic
from projectile import Projectile

# constants & libraries 
from constants import *
import pygame


# helper - shield status text 
def draw_shield_status(surface, player, font_small):
    # displays text when a player's shield is active 
    if player.has_shield:
        text = font_small.render(
            f"SHIELD ACTIVE (+{player.shield_block})",
            True,
            (0, 140, 255)
        )
        surface.blit(text, (20, 60))

# main renderer class 
# responsible for drawing the entire game each frame 
class Renderer:

# initialization 
    def __init__(self):
        
        # fonts used across UI 
        self.font_small = pygame.font.SysFont("Courier New", 14, bold=True)
        self.font_medium = pygame.font.SysFont("Courier New", 22, bold=True)
        self.font_large = pygame.font.SysFont("Courier New", 48, bold=True)
        self.font_log = pygame.font.SysFont("Courier New", 12)
        self.font_btn = pygame.font.SysFont("Courier New", 13, bold=True)
        
        # wind visual effect system 
        self.wind_effect = WindEffect()
    
    # main draw function 
    def draw(self, surface, game):
        
        # background 
        surface.fill(OFF_WHITE)

        # safe guard - ensures players exist before rendering 
        if not game.player1 or not game.player2:
            if game.state == game.TITLE:
                draw_title(surface, game, self)
            elif game.state == game.SELECT:
                self._draw_select(surface, "Player 1")
            elif game.state == game.SELECT_P2:
                self._draw_select(surface, "Player 2")
            return

        # left player HUD 
        draw_xp_bar(
            surface, 
            LEFT_X, 
            TOP_Y,
            game.player1.exp, 
            self.font_small
        )

        draw_health_bar(
            surface, 
            LEFT_X, 
            TOP_Y + 30,
            game.player1.hp, 
            game.player1.base_hp,
            game.player1.name, 
            self.font_small, 
            self.font_log
        )

        # right player HUD 
        draw_xp_bar(
            surface, 
            RIGHT_X, 
            TOP_Y,
            game.player2.exp, 
            self.font_small
        )

        draw_health_bar(
            surface, 
            RIGHT_X, 
            TOP_Y + 30,
            game.player2.hp, 
            game.player2.base_hp,
            game.player2.name, 
            self.font_small, 
            self.font_log
        )

        # game state screens
        if game.state == game.TITLE:
            draw_title(surface, game, self)
            return

        if game.state == game.SELECT:
            self._draw_select(surface, "Player 1")
            return

        if game.state == game.SELECT_P2:
            self._draw_select(surface, "Player 2")
            return

        # world elements 
        draw_ground(surface)
        draw_fence(surface, FENCE_X, GROUND_Y)

        # pickups 
        game.heal_pickup.draw(surface)
        game.shield_pickup.draw(surface)

        # experience orbs 
        for orb in game.exp_orbs:
            orb.draw(surface)

        # wind effect - clipped to sky area 
        surface.set_clip(0, 0, WIDTH, GROUND_Y)
        self.wind_effect.update(game.wind)
        self.wind_effect.draw(surface, game.wind)
        surface.set_clip(None)
        
        # player context 
        player = game._current()
        is_human = (game.turn == 0) or game.two_player
        
        # shield button - stored for click detection  
        game.shield_rect = draw_shield_button(surface, player, self.font_btn)

        # character rendering 
        draw_character(surface, PLAYER1_X, PLAYER1_Y, game.player1.name, self.font_small)
        draw_character(surface, PLAYER2_X, PLAYER2_Y, game.player2.name, self.font_small)

        # defensive visuals
        if game.player1.has_shield or game.player1.defending:
            draw_defend_bubble(surface, PLAYER1_X, PLAYER1_Y)

        if game.player2.has_shield or game.player2.defending:
            draw_defend_bubble(surface, PLAYER2_X, PLAYER2_Y)

        # aim and trajectory preview 
        draw_aim(surface, game)

        points = []
        
        # human trajectory preview - charging shot
        if is_human and game.charging:
            points = Projectile.simulate_trajectory(
                *player.aim_origin(),
                game.aim_angle,
                game.power,
                game.wind
            )
            
        # AI trajectory preview 
        elif not is_human:
            points = getattr(game.ai, "preview_points", [])

        # draws preview points (only first half - adds challenge)
        half = len(points) // 2
        for i in range(0, half, 5):
            x, y = points[i]
            if y >= GROUND_Y:
                break
            if 0 <= x <= WIDTH:
                pygame.draw.circle(surface, BLACK, (int(x), int(y)), 2)

        # active projectile 
        if game.projectile:
            game.projectile.draw(surface)

        # log panel - right side 
        draw_history_log(surface, game, self,
                        LOG_X, LOG_Y, LOG_W, LOG_H)

        # global UI - bottom area 
        draw_wind(surface, game, self.font_small)


        # player-specific UI 
        p1_dmg = game.get_damage_estimate(game.player1)
        p2_dmg = game.get_damage_estimate(game.player2)

        draw_player_ui(
            surface,
            self.font_small,
            self.font_medium,
            UI_HEAL_X,
            game.player1.name,
            p1_dmg,
            UI_BAR_Y,
            game.turn == 0
        )

        draw_player_ui(
            surface,
            self.font_small,
            self.font_medium,
            UI_SHIELD_X,
            game.player2.name,
            p2_dmg,
            UI_BAR_Y,
            game.turn == 1
        )

        # action buttons - stores rects for interaction 
        game.heal_rect = draw_heal_button(surface, player, self.font_btn)
        game.special_rect = draw_special_button(surface, player, self.font_btn)

        # game over screen 
        if game.state == game.GAME_OVER:
            draw_game_over(surface, game, self)
            

    # character selection screen 
    def _draw_select(self, surface, player_label="Player 1"):
        # draws the character selection menu 
        
        title = self.font_medium.render(f"{player_label} - Choose Character", True, BLACK)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 120))

        options = [
            f"1: Cat (HP: {CHARACTERS['Cat']['hp']})",
            f"2: Dog (HP: {CHARACTERS['Dog']['hp']})",
            f"3: Wolf (HP: {CHARACTERS['Wolf']['hp']})",
            f"4: Elephant (HP: {CHARACTERS['Elephant']['hp']})"
        ]

        for i, opt in enumerate(options):
            text = self.font_small.render(opt, True, BLACK)
            surface.blit(text, (WIDTH // 2 - 60, HEIGHT // 2 - 60 + i * 30))