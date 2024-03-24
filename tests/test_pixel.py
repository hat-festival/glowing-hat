from unittest import TestCase

from lib.pixel import Pixel


class TestPixel(TestCase):
    """Test the Pixel."""

    def test_constructor(self):
        """Test it gets the right data."""
        pix = Pixel({"index": 0, "x": 1, "y": 2, "z": -3.5})
        assert pix.data == {
            "index": 0,
            "x": 1,
            "y": 2,
            "z": -3.5,
            "hue": 1.0,
            "saturation": 1.0,
            "value": 1.0,
            "rgb": (255, 0, 0),
            "angles": {
                "x": 299.7448812969422,
                "z": 63.43494882292201,
                "y": 164.05460409907712,
            },
        }

    def test_recalculating_rgb(self):
        """Test it recalcs RGB when required."""
        pix = Pixel({"index": 0, "x": 1, "y": 2, "z": -3.5})
        assert pix["rgb"] == (255, 0, 0)

        pix["hue"] = 1 / 3
        assert pix["rgb"] == (0, 255, 0)

        pix["hue"] = 1.0
        pix["rgb"] = (0, 255, 255)
        assert pix["rgb"] == (0, 255, 255)

    def test_immutability(self):
        """Test that some fields are immutable."""
        pix = Pixel({"index": 0, "x": 1, "y": 2, "z": -3.5})
        assert pix["x"] == 1
        assert pix["hue"] == 1.0

        pix["hue"] = 0.5
        assert pix["hue"] == 0.5  # noqa: PLR2004

        pix["x"] = 0.5
        assert pix["x"] == 1

    def test_richer_construction(self):
        """Test we can provide additional constructor data."""
        data = {"index": 0, "x": 0.5, "y": 2, "z": -3.5, "hue": 0.4}
        pix = Pixel(data)
        assert pix["x"] == 0.5  # noqa: PLR2004
        assert pix["hue"] == 0.4  # noqa: PLR2004

    def test_resetting(self):
        """Test we can reset a pixels s and v."""
        data = {"index": 0, "x": 0.5, "y": 2, "z": -3.5, "hue": 0.4}
        pix = Pixel(data)

        pix["value"] = 0.5
        assert pix["hue"] == 0.4  # noqa: PLR2004
        assert pix["value"] == 0.5  # noqa: PLR2004

        pix.reset()
        assert pix["hue"] == 0.4  # noqa: PLR2004
        assert pix["value"] == 1.0
