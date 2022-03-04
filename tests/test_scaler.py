from unittest import TestCase

from lib.scaler import Scaler, deconstruct, find_largest_span


class TestScaler(TestCase):
    """Test the Scaler."""

    def test_constructor(self):
        """Test it gets the right data."""
        scaler = Scaler("tests/fixtures/conf/simple-locations.yaml")
        self.assertEqual(
            scaler.absolutes,
            {
                "lights": [
                    {"index": 0, "x": 0, "y": 0, "z": 0},
                    {"index": 1, "x": 1, "y": 1, "z": 1},
                    {"index": 2, "x": 2, "y": 2, "z": 2},
                    {"index": 3, "x": 3, "y": 3, "z": 3},
                    {"index": 4, "x": 4, "y": 4, "z": 4},
                ],
                "centres": {"x": 2, "y": 2, "z": 2},
            },
        )

    def test_simple_scaling(self):
        """Test it scales the simple data."""
        scaler = Scaler("tests/fixtures/conf/simple-locations.yaml")
        self.assertEqual(
            scaler.scaled,
            [
                {"index": 0, "x": -1, "y": -1, "z": -1},
                {"index": 1, "x": -0.5, "y": -0.5, "z": -0.5},
                {"index": 2, "x": 0, "y": 0, "z": 0},
                {"index": 3, "x": 0.5, "y": 0.5, "z": 0.5},
                {"index": 4, "x": 1, "y": 1, "z": 1},
            ],
        )


def test_find_largest_span():
    """Test it finds the largest span."""
    assert (
        find_largest_span(
            {
                "lights": [
                    {"index": 0, "x": 1, "y": 2, "z": 3},
                    {"index": 1, "x": 10, "y": 11, "z": 12},
                    {"index": 2, "x": 4, "y": 5, "z": 6},
                    {"index": 3, "x": 7, "y": 8, "z": 9},
                    {"index": 4, "x": 25, "y": 14, "z": 15},
                ],
                "centres": {"x": 7, "y": 8, "z": 9},
            }
        )
        == 18
    )


def test_deconstruct():
    """Test it breaks-up the data."""
    assert deconstruct(
        [
            {"index": 0, "x": 1, "y": 2, "z": 3},
            {"index": 1, "x": 10, "y": 11, "z": 12},
            {"index": 2, "x": 4, "y": 5, "z": 6},
            {"index": 3, "x": 7, "y": 8, "z": 9},
            {"index": 4, "x": 13, "y": 14, "z": 15},
        ]
    ) == {
        "x": [1, 10, 4, 7, 13],
        "y": [2, 11, 5, 8, 14],
        "z": [3, 12, 6, 9, 15],
    }
