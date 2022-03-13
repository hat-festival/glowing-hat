from unittest import TestCase


from lib.pixel_hat import PixelHat
from lib.renderers.bands import Band, get_intervals


class TestBand(TestCase):
    """Test it renders a single band."""

    def test_simple_rendering(self):
        """Test it renders correctly for the simple case."""
        hat = PixelHat(
            locations="tests/fixtures/bands/simplest-locations.yaml", auto_centre=True
        )
        band = Band(1, 1, "x", "up", steps=2, hat=hat)

        self.assertEqual(band, [[0], [1]])

    def test_three_location_rendering(self):
        """Test it renders with three simple locations."""
        hat = PixelHat(
            locations="tests/fixtures/bands/three-locations.yaml", auto_centre=True
        )
        band = Band(1, 1, "x", "up", steps=3, hat=hat)

        self.assertEqual(band, [[0], [1], [2]])

    def test_wider_rendering(self):
        """Test it renders a wider band."""
        hat = PixelHat(
            locations="tests/fixtures/bands/simplest-locations.yaml", auto_centre=True
        )
        band = Band(2, 1, "x", "up", steps=3, hat=hat)

        self.assertEqual(band, [[0], [0, 1], [1]])

def test_get_intervals():
    """Test the interval-getter."""
    assert get_intervals(2) == [-1, 1]
    assert get_intervals(3) == [-1, 0, 1]
    assert get_intervals(4) == [-1, -0.333, 0.333, 1]
