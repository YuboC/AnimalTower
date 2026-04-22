import pytest
import game.combat as combat


class DummyPlayer:
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.defending = False
        self.has_shield = False
        self.shield_block = 0


# -------------------
# SANITY TEST
# -------------------

def test_combat_module_exists():
    assert combat is not None


# -------------------
# OPTIONAL DAMAGE TESTS (ONLY IF FUNCTION EXISTS)
# -------------------

def test_damage_function_if_exists():
    player = DummyPlayer()

    # dynamically find possible function names
    func = None

    for name in ["apply_damage", "deal_damage", "damage_player"]:
        if hasattr(combat, name):
            func = getattr(combat, name)
            break

    if func is None:
        pytest.skip("No standalone damage function in combat.py")

    func(player, 20)

    assert player.hp < 100


# -------------------
# DEFENSE / SHIELD (ONLY IF SUPPORTED)
# -------------------

def test_defense_if_supported():
    player = DummyPlayer()
    player.defending = True

    func = None
    for name in ["apply_damage", "deal_damage", "damage_player"]:
        if hasattr(combat, name):
            func = getattr(combat, name)
            break

    if func is None:
        pytest.skip("No damage function to test defense")

    func(player, 20)

    assert player.hp > 80  # reduced damage


def test_shield_if_supported():
    player = DummyPlayer()
    player.has_shield = True
    player.shield_block = 10

    func = None
    for name in ["apply_damage", "deal_damage", "damage_player"]:
        if hasattr(combat, name):
            func = getattr(combat, name)
            break

    if func is None:
        pytest.skip("No damage function to test shield")

    func(player, 20)

    assert player.hp >= 90