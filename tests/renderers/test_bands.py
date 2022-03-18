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
        band = Band(1, "x", "up", steps=2, hat=hat)

        self.assertEqual(band, [[19], [24]])

    def test_more_steps_simple_rendering(self):
        """Test it renders correctly for the more-steps simple case."""
        hat = PixelHat(
            locations="tests/fixtures/bands/simplest-locations.yaml", auto_centre=True
        )
        band = Band(1, "x", "up", steps=4, hat=hat)

        self.assertEqual(band, [[19], [19], [24], [24]])

    def test_three_location_rendering(self):
        """Test it renders with three simple locations."""
        hat = PixelHat(
            locations="tests/fixtures/bands/three-locations.yaml", auto_centre=True
        )
        band = Band(1, "x", "up", steps=6, hat=hat)

        self.assertEqual(
            band, [[27, 35], [27, 35], [27, 35], [35, 16], [35, 16], [35, 16]]
        )

    def test_wider_rendering(self):
        """Test it renders a wider band."""
        hat = PixelHat(
            locations="tests/fixtures/bands/simplest-locations.yaml", auto_centre=True
        )
        band = Band(2, "x", "up", steps=3, hat=hat)

        self.assertEqual(band, [[19, 24], [19, 24], [19, 24]])

    def test_more_steps_simple_rendering(self):
        """Test it renders correctly for the simple case."""
        hat = PixelHat(
            locations="tests/fixtures/bands/simplest-locations.yaml", auto_centre=True
        )
        band = Band(1, "x", "up", steps=4, hat=hat)

        self.assertEqual(band, [[19], [19], [24], [24]])
