from unittest import TestCase

from lib.colour_wheel import ColourWheel
from lib.custodian import Custodian


class TestColourWheel(TestCase):
    """Test the hue-spinner."""

    def setUp(self):
        """Setup."""
        self.custodian = Custodian(namespace="test")
        self.custodian.populate(flush=True)

    def test_finding_start_hue(self):
        """Test it finds the existing hue."""
        self.custodian.set("hue", 0.777)
        wheel = ColourWheel(namespace="test")
        self.assertEqual(wheel.start_hue, 0.777)

    def test_with_no_start_hue(self):
        """Test it handles no start hue."""
        wheel = ColourWheel(namespace="test")
        self.assertEqual(wheel.start_hue, 0)

    def test_rotate(self):
        """Test it rotates."""
        self.custodian.set("hue", 0.3)
        wheel = ColourWheel(namespace="test")
        wheel.steps = 500
        wheel.rotate(testing=True)
        self.assertEqual(float(self.custodian.get("hue")), 0.29800000000000004)
