from unittest import TestCase

from lib.colour_wheel import ColourWheel
from lib.redis_manager import RedisManager


class TestColourWheel(TestCase):
    """Test the hue-spinner."""

    def setUp(self):
        """Setup."""
        self.redisman = RedisManager(namespace="test")
        self.redisman.populate(flush=True)

    def test_finding_start_hue(self):
        """Test it finds the existing hue."""
        self.redisman.enter("hue", 0.777)
        wheel = ColourWheel(namespace="test")
        self.assertEqual(wheel.start_hue, 0.777)

    def test_with_no_start_hue(self):
        """Test it handles no start hue."""
        self.redisman.unset("hue")
        wheel = ColourWheel(namespace="test")
        self.assertEqual(wheel.start_hue, 0)

    def test_rotate(self):
        """Test it rotates."""
        self.redisman.enter("hue", 0.3)
        wheel = ColourWheel(namespace="test")
        wheel.rotate(testing=True, steps=500)
        self.assertEqual(float(self.redisman.retrieve("hue")), 0.7989999999999999)
