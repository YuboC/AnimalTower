import pytest
import pygame
from game import input as game_input


# ---------------------------
# FIXED DummyGame
# ---------------------------
class DummyPlayer:
    def __init__(self):
        self.x = 100
        self.y = 100

    def aim_origin(self):
        return (self.x, self.y)


class DummyProjectile:
    def __init__(self, alive=True):
        self.alive = alive


class DummyGame:
    def __init__(self):
        self.projectile = None
        self.turn = 0
        self.player1 = DummyPlayer()
        self.player2 = DummyPlayer()

    def _current(self):
        return self.player1


# ---------------------------
# MOCK MOUSE
# ---------------------------
@pytest.fixture(autouse=True)
def mock_mouse(monkeypatch):
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (150, 200))


# ---------------------------
# TESTS
# ---------------------------
def test_update_aim_runs():
    game = DummyGame()

    game_input.update_aim(game)

    assert isinstance(game.aim_angle, float)


def test_update_aim_no_crash_with_projectile():
    game = DummyGame()
    game.projectile = DummyProjectile(alive=True)

    game_input.update_aim(game)

    # unchanged projectile should still be alive
    assert game.projectile.alive is True