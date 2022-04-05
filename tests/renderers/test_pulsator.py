from lib.renderers.pulsator import populate


def test_easy_populate():
    """Test the stupid case."""
    assert populate(4) == [0, 0.5, 1, 0.5]


def test_with_more_steps():
    """Test the more-steps case."""
    assert populate(16) == [
        0.0,
        0.038,
        0.146,
        0.309,
        0.5,
        0.691,
        0.854,
        0.962,
        1.0,
        0.962,
        0.854,
        0.691,
        0.5,
        0.309,
        0.146,
        0.038,
    ]
