import game.heal_pickup as heal_module

class FakePlayer:
    def __init__(self):
        self.name = "A"
        self.hp = 50
        self.base_hp = 100


class FakeGame:
    def __init__(self):
        self.logs = []
        self.messages = []

    def _current(self):
        return self.player

    def _log(self, msg):
        self.logs.append(msg)

    def _show_message(self, msg):
        self.messages.append(msg)


def test_heal_on_hit():
    g = FakeGame()
    player = FakePlayer()
    g.player = player

    pickup = object()

    heal_module.heal_on_hit(g, pickup)

    assert player.hp > 50  # healed
    assert "healed" in g.logs[0]
    assert "HP!" in g.messages[0]