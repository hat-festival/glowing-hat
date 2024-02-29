from lib.axis_rotator import circle, live_axes, start_corner


def test_live_axes():
    """Test it works out the axes in play."""
    assert live_axes(("z", "x")) == [2, 0]


def test_start_corner():
    """Test it works out the starting corner."""
    assert start_corner(("z", "x")) == [-1.0, 0.0, -1.0]


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


def test_richer_circle():
    """Test going round in a denser circle."""
    assert circle(("z", "x"), interval=0.5) == [
        "sorts:(-1.0, 0.0, -1.0)",  # back left
        "sorts:(-1.0, 0.0, -0.5)",
        "sorts:(-1.0, 0.0, 0.0)",
        "sorts:(-1.0, 0.0, 0.5)",
        "sorts:(-1.0, 0.0, 1.0)",  # front left
        "sorts:(-0.5, 0.0, 1.0)",
        "sorts:(0.0, 0.0, 1.0)",
        "sorts:(0.5, 0.0, 1.0)",
        "sorts:(1.0, 0.0, 1.0)",  # front right
        "sorts:(1.0, 0.0, 0.5)",
        "sorts:(1.0, 0.0, 0.0)",
        "sorts:(1.0, 0.0, -0.5)",
        "sorts:(1.0, 0.0, -1.0)",  # back right
        "sorts:(0.5, 0.0, -1.0)",
        "sorts:(0.0, 0.0, -1.0)",
        "sorts:(-0.5, 0.0, -1.0)",
    ]


def test_reverse_circle():
    """Test going round in a circle the other way."""
    assert circle(("z", "x"), interval=1, direction="backwards") == [
        "sorts:(-1.0, 0.0, -1.0)",
        "sorts:(0.0, 0.0, -1.0)",
        "sorts:(1.0, 0.0, -1.0)",
        "sorts:(1.0, 0.0, 0.0)",
        "sorts:(1.0, 0.0, 1.0)",
        "sorts:(0.0, 0.0, 1.0)",
        "sorts:(-1.0, 0.0, 1.0)",
        "sorts:(-1.0, 0.0, 0.0)",
    ]


def test_y_z_circle():
    """Test going round in a circle."""
    assert circle(("y", "z"), interval=1) == [
        "sorts:(0.0, -1.0, -1.0)",
        "sorts:(0.0, 0.0, -1.0)",
        "sorts:(0.0, 1.0, -1.0)",
        "sorts:(0.0, 1.0, 0.0)",
        "sorts:(0.0, 1.0, 1.0)",
        "sorts:(0.0, 0.0, 1.0)",
        "sorts:(0.0, -1.0, 1.0)",
        "sorts:(0.0, -1.0, 0.0)",
    ]
