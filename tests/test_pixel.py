from unittest import TestCase

from lib.pixel import Pixel

DATA = {"index": 0, "x": 1, "y": 2, "z": -3.5}


class TestPixel(TestCase):
    """Test the Pixel."""

    def test_constructor(self):
        """Test it gets the right data."""
        pix = Pixel(DATA)
        self.assertEqual(pix.data, {"index": 0, "x": 1, "y": 2, "z": -3.5})

    def test_greater_than(self):
        """Test `greater_than`."""
        pix = Pixel(DATA)
        self.assertTrue(pix.greater_than("x", 0.5))
        self.assertTrue(pix.greater_than("y", 2))
        self.assertFalse(pix.greater_than("z", -2))

    def test_less_than(self):
        """Test `less_than`."""
        pix = Pixel(DATA)
        self.assertTrue(pix.less_than("x", 2.5))
        self.assertFalse(pix.less_than("y", 2))
        self.assertFalse(pix.less_than("z", -20))
