import sys, types

mock_audio = types.ModuleType("game.audio")
mock_audio.load_sound = lambda *a, **k: None
mock_audio.play_sound = lambda *a, **k: None
sys.modules["game.audio"] = mock_audio

import game.game_state as gs
from game.combat import check_collisions
from tests.fakes import FakeProjectile, FakePlayer, FakeAI


def make_game():
    g = gs.Game()

    g.player1 = FakePlayer("A")
    g.player2 = FakePlayer("B")

    g.ai = FakeAI()

    g.projectile = FakeProjectile()
    g.state = gs.Game.PLAYING
    g.turn = 0

    return g


def test_projectile_runs():
    g = make_game()
    check_collisions(g)
    assert g.projectile is not None


def test_projectile_missing_does_not_crash():
    g = make_game()
    g.projectile.y = 9999
    check_collisions(g)
    assert True