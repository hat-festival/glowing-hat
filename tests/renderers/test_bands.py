from unittest import TestCase

from lib.pixel_hat import PixelHat
from lib.renderers.bands import Band


class TestBand(TestCase):
    """Test it renders a single band."""

    def test_simple_rendering(self):
        """Test it renders correctly for the simple case."""
        hat = PixelHat(
            locations="tests/fixtures/bands/simplest-locations.yaml", auto_centre=True
        )
        band = Band(1, 1, "x", "up", hat)

        self.assertEqual(band, [[], [0], [1], []])

    def test_three_location_rendering(self):
        """Test it renders with three simple locations."""
        hat = PixelHat(
            locations="tests/fixtures/bands/three-locations.yaml", auto_centre=True
        )
        band = Band(1, 1, "x", "up", hat)

        self.assertEqual(band, [[], [0], [1], [2], []])
