from lib.tools import gamma_correct, hue_to_grb


def test_hue_to_grb():
    """Test it turns a `hue` value into a GRB triple."""
    cases = (
        (0, [0, 255, 0]),
        (0.5, [255, 0, 255]),
    )

    for hue, grb in cases:
        assert hue_to_grb(hue) == grb


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
