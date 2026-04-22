import pytest

from player import Player


# BASIC INITIALIZATION
def test_player_initialization():
    p = Player("Cat", 100, 200, 10, 45)

    assert p.name == "Cat"
    assert p.hp == 100
    assert p.max_hp == 100
    assert p.exp == 0


# APPLY STATS
def test_apply_stats_hp_and_atk():
    p = Player("Cat", 0, 0, 0, 0)

    p.apply_stats({
        "hp": 20,
        "atk": 5,
        "defense": 3,
        "special_bonus": 1.5
    })

    assert p.base_hp == 120
    assert p.atk == 15
    assert p.defense == 8
    assert p.special_bonus == 1.5


# DAMAGE LOGIC
def test_take_damage_normal():
    p = Player("Cat", 0, 0, 0, 0)

    dmg = p.take_damage(30)

    assert dmg == 30
    assert p.hp == 70


def test_take_damage_defending():
    p = Player("Cat", 0, 0, 0, 0)
    p.defending = True

    dmg = p.take_damage(30)

    assert dmg == 15
    assert p.hp == 85  # 100 - 15


def test_take_damage_shield_blocks():
    p = Player("Cat", 0, 0, 0, 0)
    p.has_shield = True

    dmg = p.take_damage(50)

    assert dmg == 0
    assert p.hp == 100
    assert p.has_shield is False


def test_hp_never_negative():
    p = Player("Cat", 0, 0, 0, 0)

    p.take_damage(999)

    assert p.hp == 0
    assert p.is_dead() is True


# HEAL SYSTEM
def test_heal_basic():
    p = Player("Cat", 0, 0, 0, 0)
    p.hp = 40

    healed = p.heal()

    assert healed > 0
    assert p.hp > 40


def test_heal_spends_xp():
    p = Player("Cat", 0, 0, 0, 0)
    p.hp = 50
    p.exp = 100

    first = p.heal()
    assert first > 0
    assert p.exp == 0  # XP spent

    # can't heal again without XP
    assert p.can_heal() is False


def test_heal_at_full_hp():
    p = Player("Cat", 0, 0, 0, 0)

    healed = p.heal()

    assert healed == 0


# UI HELPERS
def test_aim_origin():
    p = Player("Cat", 100, 200, 10, 45)

    x, y = p.aim_origin()

    assert x == 110
    assert y == 185


def test_get_ui_positions():
    p = Player("Cat", 100, 200, 10, 45)

    label_x, label_y, btn_x, btn_y = p.get_ui_positions()

    assert label_x == 100
    assert label_y == 235
    assert btn_x == 70
    assert btn_y == 260


# XP SYSTEM
def test_add_exp_caps_at_heal_cost():
    p = Player("Cat", 0, 0, 0, 0)

    p.add_exp(50)
    assert p.exp == 50

    p.add_exp(200)
    assert p.exp == 100  # capped at XP_HEAL_COST


def test_can_heal_requires_full_xp():
    p = Player("Cat", 0, 0, 0, 0)
    p.hp = 50

    assert p.can_heal() is False  # no XP

    p.exp = 100
    assert p.can_heal() is True  # full XP + damaged

    p.hp = 100
    assert p.can_heal() is False  # full HP