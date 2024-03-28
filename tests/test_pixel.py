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
            "hue": 0.0,
            "saturation": 1.0,
            "value": 1.0,
            "angles": {
                "x": 299.7448812969422,
                "z": 63.43494882292201,
                "y": 164.05460409907712,
            },
        }

    def test_immutability(self):
        """Test that some fields are immutable."""
        pix = Pixel({"index": 0, "x": 1, "y": 2, "z": -3.5})
        assert pix["x"] == 1
        assert pix["hue"] == 0.0

        pix["hue"] = 0.5
        assert pix["hue"] == 0.5  # noqa: PLR2004

        pix["x"] = 0.5
        assert pix["x"] == 1

    def test_it_gives_only_good_data(self):
        """Test it knows when it doesn't have something."""
        pix = Pixel({"index": 0, "x": 1, "y": 2, "z": -3.5})
        assert not pix["banana"]

    def test_richer_construction(self):
        """Test we can provide additional constructor data."""
        data = {"index": 0, "x": 0.5, "y": 2, "z": -3.5, "hue": 0.4}
        pix = Pixel(data)
        assert pix["x"] == 0.5  # noqa: PLR2004
        assert pix["hue"] == 0.4  # noqa: PLR2004

    def test_hue_from_angle(self):
        """Test it knows how to get a hue from an angle."""
        data = {"index": 0, "x": 0.0, "y": 1.0, "z": 1.0}
        pix = Pixel(data)
        assert pix["angles"]["y"] == 360  # noqa: PLR2004

        pix.hue_from_angle()
        assert pix["hue"] == 0.0

        pix.hue_from_angle(offset=90)
        assert pix["hue"] == 0.25  # noqa: PLR2004
