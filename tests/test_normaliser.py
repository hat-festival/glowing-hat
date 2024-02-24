from unittest import TestCase

from lib.colour_normaliser import ColourNormaliser
from lib.tools import close_enough


class TestColourNormaliser(TestCase):
    """Test the normaliser."""

    def test_init(self):
        """Test the constructor."""
        norm = ColourNormaliser()
        assert norm.max_brightness.value == 0.5  # noqa: PLR2004
        assert close_enough(norm.default_brightness.value, 0.15)

    def test_recalculate_brightness_down(self):
        """Test the brightness recalculator."""
        norm = ColourNormaliser()
        norm.adjust_brightness("down")
        assert close_enough(norm.max_brightness.value, 0.45, tolerance=0.000001)

    def test_recalculate_brightness_up(self):
        """Test the brightness recalculator."""
        norm = ColourNormaliser()
        norm.max_brightness.value = 0.1
        norm.adjust_brightness("up")
        assert close_enough(norm.max_brightness.value, 0.15, tolerance=0.000001)

    def test_recalculate_brightness_down_at_limit(self):
        """Test the brightness recalculator."""
        norm = ColourNormaliser()
        norm.max_brightness.value = 0.05
        norm.adjust_brightness("down")
        assert close_enough(norm.max_brightness.value, 0.0, tolerance=0.000001)

    def test_recalculate_brightness_up_at_limit(self):
        """Test the brightness recalculator."""
        norm = ColourNormaliser()
        norm.adjust_brightness("up")
        assert close_enough(norm.max_brightness.value, 0.5, tolerance=0.000001)
