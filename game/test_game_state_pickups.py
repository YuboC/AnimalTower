import sys, types

mock_audio = types.ModuleType("game.audio")
mock_audio.load_sound = lambda *a, **k: None
mock_audio.play_sound = lambda *a, **k: None
sys.modules["game.audio"] = mock_audio

import game.game_state as gs
from tests.fakes import FakeProjectile, FakePlayer, FakeAI


class FakeOrb:
    def __init__(self):
        self.updated = False
        self.collected = False
        self.value = 10

    def update(self, wind):
        self.updated = True

    def attract(self, player):
        pass

    def collides_with_projectile(self, proj):
        return False

    def collect(self):
        self.collected = True

    def reset(self):
        self.collected = True   # or just pass


def make_game():
    g = gs.Game()

    g.state = gs.Game.PLAYING
    g.player1 = FakePlayer("A")
    g.player2 = FakePlayer("B")

    g.ai = FakeAI()

    g.exp_orbs = [FakeOrb(), FakeOrb()]
    g.projectile = FakeProjectile()

    return g


def test_orbs_update():
    g = make_game()
    g.update()
    assert all(o.updated for o in g.exp_orbs)


def test_orb_collection_logic():
    g = make_game()

    orb = g.exp_orbs[0]
    orb.collides_with_projectile = lambda p: True

    g.update()

    assert orb.collected is True