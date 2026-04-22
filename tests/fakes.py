class FakeProjectile:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.alive = True

    def check_hit(self, x, y, r):
        return False


class FakePlayer:
    def __init__(self, name="A"):
        self.name = name

        self.x = 100
        self.y = 100

        self.hp = 100
        self.base_hp = 100

        self.default_aim_angle = 0

        self.defending = False
        self.heal_used = False

        self.special_active = False
        self.special_cooldown = 0

        self.has_shield = False
        self.shield_block = 0
        self.shield_used = False

        self.max_specials = 2
        self.special_used = 0

        self.exp = 0

    def reset(self):
        self.hp = self.base_hp
        self.defending = False
        self.special_active = False
        self.exp = 0

    def is_dead(self):
        return self.hp <= 0

    def take_damage(self, dmg):
        self.hp -= dmg
        return dmg

    def heal(self):
        self.hp += 10
        return 10

    def can_attack(self):
        return True

    def add_exp(self, val):
        self.exp = getattr(self, "exp", 0) + val


class FakeAI:
    def __init__(self):
        self.reset_called = False

    def reset(self):
        self.reset_called = True

    def update(self, game):
        pass