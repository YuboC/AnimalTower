import game.physics as physics

from constants import GRAVITY
from constants import WIND_FACTOR
from game.physics import is_out_of_bounds

class FakeProjectile:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.vx = 2
        self.vy = -5
        self.alive = True


class FakeGame:
    def __init__(self):
        self.projectile = FakeProjectile()
        self.wind = 0   # deterministic
        
class FakeP:
    def __init__(self, y):
        self.y = y

        
# testing projectile movement 
def test_projectile_moves():
    g = FakeGame()

    physics.update_projectile(g)

    p = g.projectile

    assert p.x != 100
    assert p.y != 100
    
    
# testing gravity affecting velocity 
def test_gravity_applied():
    g = FakeGame()

    old_vy = g.projectile.vy

    physics.update_projectile(g)

    assert g.projectile.vy == old_vy + GRAVITY
    
    
# testing for how wind affects vx
def test_wind_affects_velocity():
    g = FakeGame()
    g.wind = 2

    old_vx = g.projectile.vx

    physics.update_projectile(g)

    assert g.projectile.vx == old_vx + (2 * WIND_FACTOR)
    
# testing if inactive projectile does nothing 
def test_inactive_projectile():
    g = FakeGame()
    g.projectile.alive = False

    result = physics.update_projectile(g)

    assert result is False
    

# testing for if it goes out of bounds
def test_out_of_bounds_true():
    p = FakeP(9999)
    assert is_out_of_bounds(p) is True


def test_out_of_bounds_false():
    p = FakeP(10)
    assert is_out_of_bounds(p) is False