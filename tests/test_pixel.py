from unittest import TestCase

from lib.pixel import Pixel


class TestPixel(TestCase):
    """Test the Pixel."""

    def test_constructor(self):
        """Test it gets the right data."""
        pix = Pixel(0, 1, 2, -3.5)
        self.assertEqual(pix.index, 0)
        self.assertEqual(pix.location, {"x": 1, "y": 2, "z": -3.5})

    def test_greater_than(self):
        """Test `greater_than`."""
        pix = Pixel(0, 1, 2, -3.5)
        self.assertTrue(pix.greater_than("x", 0.5))
        self.assertTrue(pix.greater_than("y", 2))
        self.assertFalse(pix.greater_than("z", -2))

    def test_less_than(self):
        """Test `less_than`."""
        pix = Pixel(0, 1, 2, -3.5)
        self.assertTrue(pix.less_than("x", 2.5))
        self.assertTrue(pix.less_than("y", 2))
        self.assertFalse(pix.less_than("z", -20))
