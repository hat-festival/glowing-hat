from unittest import TestCase

from lib.scaler import Scaler


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
