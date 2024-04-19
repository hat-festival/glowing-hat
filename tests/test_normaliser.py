from unittest import TestCase

from glowing_hat.brightness_controllers.brightness_control import BrightnessControl
from glowing_hat.tools.utils import close_enough


class TestColourNormaliser(TestCase):
    """Test the brightness_controller."""

    def test_initialisation(self):
        """Test it starts at 50%."""
        norm = BrightnessControl()
        assert norm.factor.value == 0.5  # noqa: PLR2004
        assert norm.max_brightness.value == 1.0

    def test_turn_brightness_down(self):
        """Test turning brightness down."""
        norm = BrightnessControl()
        norm.adjust("down")
        assert close_enough(norm.factor.value, 0.40, tolerance=0.000001)

    def test_turn_brightness_up(self):
        """Test turning brightness up."""
        norm = BrightnessControl()
        norm.factor.value = 0.1
        norm.adjust("up")
        assert close_enough(norm.factor.value, 0.20, tolerance=0.000001)

    def test_turn_brightness_down_at_limit(self):
        """Test turning brightness down at limit."""
        norm = BrightnessControl()
        norm.factor.value = 0.05
        norm.adjust("down")
        assert close_enough(norm.factor.value, 0.0, tolerance=0.000001)

    def test_turn_brightness_up_at_limit(self):
        """Test turning brightness up at limit."""
        norm = BrightnessControl()
        norm.factor.value = 0.95
        norm.adjust("up")
        assert close_enough(norm.factor.value, 1.0, tolerance=0.000001)
