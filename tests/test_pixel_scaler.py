from unittest import TestCase

from lib.pixel_scaler import PixelScaler


class TestPixelScaler(TestCase):
    """Test the PixelScaler."""

    def test_constructor(self):
        """Test it gets the correct data."""
        scaler = PixelScaler("tests/fixtures/scaler/simple.yaml")

        self.assertEqual(
            scaler.absolutes[0], {"index": 0, "x": 1348.0, "y": 999.0, "z": 648.0}
        )
