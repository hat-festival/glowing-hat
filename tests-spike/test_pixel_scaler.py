from unittest import TestCase

from lib.pixel_scaler import PixelScaler, limits, scale, split


class TestPixelScaler(TestCase):
    """Test the PixelScaler."""

    def test_constructor(self):
        """Test it gets the correct data."""
        scaler = PixelScaler("tests/fixtures/scaler/simple.yaml")

        self.assertEqual(
            scaler.absolutes[0], {"index": 0, "x": 1348.0, "y": 999.0, "z": 648.0}
        )


def test_limits():
    """Test it finds the limits."""
    test_data = {
        "x": [25.0, -440.0, 3.0, 12.6],
        "y": [1.0, -40.0, 35.0, 11.2],
        "z": [25.0, -440.0, 3.0, 12.6],
    }

    assert limits(test_data) == {
        "x": {"max": 25.0, "min": -440.0},
        "y": {"max": 35.0, "min": -40.0},
        "z": {"max": 25.0, "min": -440.0},
    }


def test_scale():
    """Test it scales some items."""
    # cases = (
    #     ([1, 2], 1.5, [-1, 1]),
    #     ([0, 1, 2], 1, [-1, 0, 1]),
    #     ([0, 2, 4], 2, [-1, 0, 1]),
    #     ([1, 2, 3], 2, [-1, 0, 1]),
    #     # ([0, 1, 2, 3, 4, 8],  [-1.0, -0.75, -0.5, -0.25, 0.0, 1.0]),
    #     # ([4, 2, 3, 8, 0, 1], [0.0, -0.5, -0.25, 1.0, -1.0, -0.75]),
    # )

    # for items, centre, expected in cases:
    #     assert scale(items, centre) == expected

    # off_centre_cases = (([0, 1, 2], 0, [0, 0.5, 1]),)
    # for items, centre, expected in off_centre_cases:
    #     assert scale(items, centre) == expected

    # more_cases = (
    #     ([1, 2], 1, [-1, 1]),
    #     ([1, 2], 2, [-2, 2]),
    #     ([1, 2], 0.5, [-0.5, 0.5]),
    #     ([0, 1, 2, 3, 4, 8], 2, [-2.0, -1.5, -1.0, -0.5, 0.0, 2.0]),
    #     ([0, 1, 2, 3, 4, 8], 0.5, [-0.5, -0.375, -0.25, -0.125, 0.0, 0.5]),
    # )
    # for items, factor, expected in more_cases:
    #     assert scale(items, factor) == expected

    real_cases = (
        (
            [1348.0, 1642.0, 1629.0, 1437.0, 1001.0, 863.0, 1072.0, 1553.0, 1734.0],
            1,
            [],
        ),
        ([999.0, 774.5, 551.0, 477.5, 533.0, 676.0, 782.5, 652.5, 785.0], 1, []),
        ([648.0, 833.0, 1267.0, 1645.0, 1587.0, 1137.0, 770.0, 832.0, 1216.0], 2, []),
    )
    for items, factor, expected in real_cases:
        assert scale(items, factor) == expected


def test_split():
    """Test it splits some lists."""
    cases = (
        ([0, 1, 2], 1, {"bigger": [1, 2], "littler": [0]}),
        ([0, 1, 2], 1, {"bigger": [1, 2], "littler": [0]}),
    )

    for items, centre, expected in cases:
        assert split(items, centre) == expected
