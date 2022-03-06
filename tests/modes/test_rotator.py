from math import sqrt

from lib.modes.rotator import line


def test_flat_line():
    """Test a flat line."""
    assert close_enough(line(0, 2), [(0.0, 0.0), (1.0, 0.0)])


def test_45_degree_line():
    """Test a 45-degree line."""
    assert close_enough(line(45, 2), [(0, 0), ((sqrt(2) / 2), sqrt(2) / 2)])


def test_vertical_line():
    """Test a vertical line."""
    assert close_enough(line(90, 2), [(0.0, 0.0), (0.0, 1.0)])

def test_populated_line():
    """Test it generates more points."""
    assert close_enough(
        line(0, 3),
        [(0.0, 0.0), (0.5, 0.0), (1.0, 0.0)]
    )

###


def close_enough(actual, expected):
    """These numbers are fucking fiddly."""
    for i in range(len(expected)):
        for j in range(len(expected[i])):
            if abs(expected[i][j] - actual[i][j]) > 0.0000001:
                return False

    return True
