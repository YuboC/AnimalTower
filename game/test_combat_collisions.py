import pytest
from unittest.mock import patch
import game.combat as combat
from constants import *


# =========================================================
# DETERMINISTIC FAKE OBJECTS
# =========================================================

class FakePickup:
    def __init__(self, active=True, should_collide=True):
        self.active = active
        self._should_collide = should_collide

    def collides_with(self, proj):
        return self._should_collide


class FakeProjectile:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.alive = True

    def check_hit(self, x, y, r):
        return False


class FakePlayer:
    def __init__(self, name="A"):
        self.name = name
        self.x = 100
        self.y = 100
        self.has_shield = False
        self.shield_block = 0
        self.special_active = False
        self.hp = 100
        self.base_hp = 100

    def take_damage(self, dmg):
        return dmg

    def heal(self):
        return 10


class FakeGame:
    def __init__(self, projectile=None):
        self.projectile = projectile
        self.heal_pickup = FakePickup()
        self.shield_pickup = FakePickup()
        self.power = 10
        self.sound_hit = None
        self.sound_miss = None

    def _log(self, msg): pass
    def _show_message(self, msg): pass

    def _current(self):
        return FakePlayer("A")

    def _opponent(self):
        return FakePlayer("B")


# =========================================================
# TESTS
# =========================================================

def test_no_projectile():
    g = FakeGame(projectile=None)

    assert combat.check_collisions(g) is None


def test_fence_collision():
    p = FakeProjectile(FENCE_X, GROUND_Y)
    g = FakeGame(projectile=p)

    combat.check_collisions(g)

    assert p.alive is False


@patch("game.combat.heal_on_hit")
def test_heal_pickup(mock_heal):
    p = FakeProjectile(0, 0)
    g = FakeGame(projectile=p)

    g.heal_pickup.active = True
    g.heal_pickup._should_collide = True

    combat.check_collisions(g)

    mock_heal.assert_called_once()
    assert p.alive is False
    assert g.heal_pickup.active is False


# @patch("game.shield_pickup.random.randint", return_value=10)
# def test_shield_pickup(mock_rand):
#     p = FakeProjectile(0, 0)
#     g = FakeGame(projectile=p)

#     g.shield_pickup.active = True
#     g.shield_pickup._should_collide = True

#     player = FakePlayer("A")
#     player.has_shield = False
#     g._current = lambda: player

#     combat.check_collisions(g)

#     assert p.alive is False
#     assert g.shield_pickup.active is False
#     assert player.has_shield is True
#     assert player.shield_block == 10


@patch("game.combat.random.randint", return_value=10)
@patch("game.combat.random.uniform", return_value=0)
def test_opponent_hit(mock_uniform, mock_rand):
    p = FakeProjectile(0, 0)
    g = FakeGame(projectile=p)

    attacker = FakePlayer("A")
    target = FakePlayer("B")

    g._current = lambda: attacker
    g._opponent = lambda: target

    combat.check_collisions(g)

    assert p.alive is False


def test_ground_miss():
    p = FakeProjectile(0, GROUND_Y + 10)
    g = FakeGame(projectile=p)

    combat.check_collisions(g)

    assert p.alive is False