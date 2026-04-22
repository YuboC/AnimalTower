import pytest
import pygame
from game.game_state import Game


# ---------------------------------------------------
# FIX: Disable pygame mouse dependency in unit tests
# ---------------------------------------------------
@pytest.fixture(autouse=True)
def disable_pygame_mouse(monkeypatch):
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (0, 0))


# ---------------------------------------------------
# Dummy Player (matches real Game expectations)
# ---------------------------------------------------
class DummyPlayer:
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.base_hp = 100

        self.name = "P"
        self.default_aim_angle = 0

        self.x = 100
        self.y = 100

        self.defending = False
        self.heal_used = False

        self.has_shield = False
        self.shield_block = 0
        self.shield_used = False

        self.special_active = False
        self.special_used = 0
        self.max_specials = 2
        self.special_cooldown = 0

    def aim_origin(self):
        return (self.x, self.y)

    def reset(self):
        pass

    def is_dead(self):
        return self.hp <= 0

    def add_exp(self, value):
        pass

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return dmg


# ---------------------------------------------------
# Game setup helper
# ---------------------------------------------------
def setup_game():
    game = Game()

    game.player1 = DummyPlayer()
    game.player2 = DummyPlayer()

    game.state = Game.PLAYING

    return game


# ---------------------------------------------------
# TEST 1: Full attack flow
# ---------------------------------------------------
def test_full_attack_flow():
    game = setup_game()

    start_turn = game.turn

    game.aim_angle = 0
    game.power = 10

    game.handle_fire()

    assert game.projectile is not None

    for _ in range(50):
        game.update()
        if game.projectile is None:
            break

    assert game.turn != start_turn


# ---------------------------------------------------
# TEST 2: Game loop stability
# ---------------------------------------------------
def test_game_does_not_crash_on_update_loop():
    game = setup_game()

    for _ in range(100):
        game.update()

    assert True


# ---------------------------------------------------
# TEST 3: HP changes after hit
# ---------------------------------------------------
def test_player_hp_changes_after_hit():
    game = setup_game()

    p1 = game.player1
    p2 = game.player2

    game.aim_angle = 0
    game.power = 20

    game.handle_fire()

    for _ in range(100):
        game.update()
        if game.projectile is None:
            break

    assert p1.hp < p1.max_hp or p2.hp < p2.max_hp