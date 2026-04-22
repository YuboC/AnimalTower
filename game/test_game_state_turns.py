import sys, types

mock_audio = types.ModuleType("game.audio")
mock_audio.load_sound = lambda *a, **k: None
mock_audio.play_sound = lambda *a, **k: None
sys.modules["game.audio"] = mock_audio

import game.game_state as gs
from tests.fakes import FakePlayer, FakeAI


def make_game():
    g = gs.Game()

    g.player1 = FakePlayer("A")
    g.player2 = FakePlayer("B")

    g.ai = FakeAI()

    g.turn = 0
    g.turn_number = 1
    g.power = 50
    g.charging = True
    g.projectile = object()

    return g


def test_switch_turn():
    g = make_game()

    g._switch_turn()

    assert g.turn == 1
    assert g.turn_number == 2
    assert g.power == 0
    assert g.charging is False
    assert g.projectile is None
    assert g.ai.reset_called is True