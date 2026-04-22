import pytest
from game.exp_orb import ExpOrb


class DummyPlayer:
    def __init__(self):
        self.x = 100
        self.y = 100


def test_orb_creation():
    orb = ExpOrb()
    assert 10 <= orb.value <= 50


def test_orb_reset_generates_valid_value():
    orb = ExpOrb()
    old_value = orb.value

    orb.reset()

    # value should be random but valid range
    assert 10 <= orb.value <= 50


def test_orb_attract_does_not_crash():
    orb = ExpOrb()
    player = DummyPlayer()

    orb.attract(player)

    assert True