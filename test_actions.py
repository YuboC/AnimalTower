import pytest
from game import actions


class DummyPlayer:
    def __init__(self):
        self.defending = False
        self.name = "TestPlayer"
        self.heal_used = False
        self.shield_used = False
        self.has_shield = False
        self.shield_block = 0
        self.hp = 50
        self.base_hp = 100
        self.exp = 100  # full XP by default

    def heal(self):
        heal_amount = max(1, (self.base_hp - self.hp) // 2)
        self.hp = min(self.base_hp, self.hp + heal_amount)
        self.exp = 0
        return heal_amount

    def can_heal(self):
        return self.exp >= 100 and self.hp < self.base_hp

    def aim_origin(self):
        return (0, 0)


class DummyGame:
    def __init__(self):
        self.player = DummyPlayer()
        self.log = []
        self.messages = []
        self.projectile = None

        # needed for fire()
        self.aim_angle = 45
        self.power = 10
        self.wind = 0
        self.sound_throw = None

        self.switched = False

    def _current(self):
        return self.player

    def _log(self, msg):
        self.log.append(msg)

    def _show_message(self, msg):
        self.messages.append(msg)

    def _switch_turn(self):
        self.switched = True


# ======================
# DEFEND
# ======================

def test_defend_sets_flag_and_switches_turn():
    game = DummyGame()

    actions.defend(game)

    assert game.player.defending is True
    assert game.switched is True


def test_defend_logs_message():
    game = DummyGame()

    actions.defend(game)

    assert "defending" in game.log


# ======================
# SHIELD
# ======================

def test_activate_shield_success():
    game = DummyGame()
    player = game.player

    result = actions.activate_shield(game, player)

    assert result is True
    assert player.has_shield is True
    assert player.shield_used is True
    assert player.shield_block > 0


def test_activate_shield_fails_if_used():
    game = DummyGame()
    player = game.player
    player.shield_used = True

    result = actions.activate_shield(game, player)

    assert result is False
    assert len(game.messages) > 0


# ======================
# HEAL
# ======================

def test_try_heal_success():
    game = DummyGame()
    game.player.exp = 100  # full XP
    game.player.hp = 50    # damaged

    actions.try_heal(game)

    assert game.player.exp == 0  # XP spent
    assert len(game.log) > 0


def test_try_heal_no_xp():
    game = DummyGame()
    game.player.exp = 0  # no XP
    game.player.hp = 50

    actions.try_heal(game)

    assert "xp" in game.messages[0].lower()


# ======================
# FIRE
# ======================

def test_fire_creates_projectile(monkeypatch):
    game = DummyGame()

    created = {}

    class FakeProjectile:
        def __init__(self, *args, **kwargs):
            created["called"] = True

    monkeypatch.setattr(actions, "Projectile", FakeProjectile)

    actions.fire(game)

    assert created.get("called", False)


def test_fire_does_nothing_if_projectile_exists():
    game = DummyGame()
    game.projectile = object()  # already exists

    actions.fire(game)

    # should not overwrite
    assert game.projectile is not None