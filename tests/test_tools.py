from lib.tools import close_enough, gamma_correct, hue_to_rgb


def test_hue_to_rgb():
    """Test it turns a `hue` value into an RGB triple."""
    cases = (
        (0, [255, 0, 0]),
        (0.5, [0, 255, 255]),
    )

    for hue, rgb in cases:
        assert hue_to_rgb(hue) == rgb


def test_gamma_correction():
    """Test it gamma-corrects correctly."""
    cases = (
        ([0, 0, 0], [0, 0, 0]),
        ([255, 255, 255], [255, 255, 255]),
        ([255, 0, 255], [255, 0, 255]),
        ([12, 34, 56], [0, 1, 4]),
        ([112, 134, 156], [25, 42, 64]),
        ([250, 251, 252], [241, 244, 247]),
    )

    for colour, corrected in cases:
        assert gamma_correct(colour) == corrected


def test_close_enough():
    """Test it knows if a thing is close enough."""
    assert close_enough(0.01, 0) == True
    assert close_enough(0.05, 0) == True
    assert close_enough(0.1, 0, tolerance=0.05) == False
    assert close_enough(0.51, 0.5) == True
    assert close_enough(0.49, 0.5) == True
    assert close_enough(0.44, 0.5) == True
    assert close_enough(-0.51, -0.5) == True
    assert close_enough(-0.44, -0.5, tolerance=0.01) == False
