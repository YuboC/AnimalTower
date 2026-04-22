import math
from game import utils


def test_clamp_below_min():
    assert utils.clamp(5, 10, 20) == 10


def test_clamp_above_max():
    assert utils.clamp(25, 10, 20) == 20


def test_clamp_within_range():
    assert utils.clamp(15, 10, 20) == 15


def test_distance_zero():
    assert utils.distance(0, 0, 0, 0) == 0


def test_distance_3_4_5():
    assert math.isclose(utils.distance(0, 0, 3, 4), 5)


def test_lerp_start():
    assert utils.lerp(10, 20, 0) == 10


def test_lerp_end():
    assert utils.lerp(10, 20, 1) == 20


def test_lerp_middle():
    assert utils.lerp(10, 20, 0.5) == 15


def test_format_turn():
    result = utils.format_turn(1, "Cat", "Attack")
    assert result == "[T1] Cat: Attack"