from lib.axis_rotator import circle, start_corner


def test_start_corner():
    """Test it works out the starting corner."""
    assert start_corner(("z", "x")) == (-1.0, 0.0, -1.0)


def test_simple_circle():
    """Test going round in a circle."""
    assert circle(("z", "x"), interval=1) == [
        "sorts:(-1.0, 0.0, -1.0)",  # back left
        "sorts:(-1.0, 0.0, 0.0)",
        "sorts:(-1.0, 0.0, 1.0)",  # front left
        "sorts:(0.0, 0.0, 1.0)",
        "sorts:(1.0, 0.0, 1.0)",  # front right
        "sorts:(1.0, 0.0, 0.0)",
        "sorts:(1.0, 0.0, -1.0)",  # back right
        "sorts:(0.0, 0.0, -1.0)",
    ]
