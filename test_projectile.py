import math
import pytest
from projectile import Projectile


# =========================
# INIT TEST
# =========================
def test_projectile_init():
    p = Projectile(100, 100, math.pi/4, 10, 1)

    assert isinstance(p.x, float)
    assert isinstance(p.y, float)
    assert p.wind == 1
    assert p.alive is True


# =========================
# UPDATE PHYSICS
# =========================
def test_projectile_update_moves():
    p = Projectile(100, 100, 0, 10, 0)

    old_x, old_y = p.x, p.y
    p.update()

    assert p.x != old_x
    assert p.y != old_y


def test_projectile_gravity_applies():
    p = Projectile(100, 100, 0, 10, 0)

    old_vy = p.vy
    p.update()

    assert p.vy > old_vy  # gravity increases downward velocity


def test_projectile_wind_applies():
    p = Projectile(100, 100, 0, 10, 5)

    old_vx = p.vx
    p.update()

    assert p.vx != old_vx


def test_projectile_kills_out_of_bounds():
    p = Projectile(100, 100, 0, 10, 0)

    # force out of bounds
    p.x = -1000
    p.update()

    assert p.alive is False


# =========================
# HIT DETECTION
# =========================
def test_check_hit_true():
    p = Projectile(100, 100, 0, 10, 0)

    assert p.check_hit(100, 100, 10) is True


def test_check_hit_false():
    p = Projectile(0, 0, 0, 10, 0)

    assert p.check_hit(200, 200, 10) is False


# =========================
# TRAJECTORY SIMULATION
# =========================
def test_simulate_trajectory_returns_points():
    points = Projectile.simulate_trajectory(0, 0, 0, 10, 0)

    assert isinstance(points, list)
    assert len(points) > 0
    assert isinstance(points[0], tuple)


def test_simulation_stops_out_of_bounds():
    points = Projectile.simulate_trajectory(0, 0, 0, 10, 0)

    # should stop eventually or stay bounded in list form
    assert len(points) <= 200


# =========================
# ANGLE SOLVER
# =========================
def test_solve_launch_angle_returns_tuple():
    angle, dist = Projectile.solve_launch_angle(0, 0, 100, 100, 10, 0)

    assert isinstance(angle, float)
    assert isinstance(dist, float)
    assert dist >= 0


def test_solve_launch_angle_reasonable_angle():
    angle, _ = Projectile.solve_launch_angle(0, 0, 100, 100, 10, 0)

    assert -math.pi <= angle <= 0