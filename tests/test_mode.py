from unittest import TestCase

from lib.conf import conf
from lib.custodian import Custodian
from lib.hat import Hat
from lib.modes.cuttlefish import Cuttlefish


class TestFish(TestCase):
    """Test the Cuttlefish."""

    def setUp(self):
        self.custodian = Custodian(namespace="test", conf=conf)
        self.custodian.populate(flush=True)

    def test_data(self):
        """Test it gets the correct inherited data."""
        fish = Cuttlefish(Hat(), self.custodian)

        self.assertEqual(fish.name, "cuttlefish")
        self.assertEqual(
            fish.data,
            {"jump": 2, "prefs": {"axis": "y", "invert": False}, "steps": 200},
        )
        self.assertEqual(fish.prefs, {"axis": "y", "invert": False})

    def test_resetting(self):
        """Test it resets correctly."""
        fish = Cuttlefish(Hat(), self.custodian)
        fish.reset()

        self.assertFalse(self.custodian.get("invert"))
        self.assertFalse(fish.invert)

        self.assertEqual(self.custodian.get("axis"), "y")
        self.assertEqual(fish.axis, "y")

        self.assertEqual(self.custodian.get("colour-source"), "none")

    def test_reconfiguring(self):
        """Test it reconfigures correctly."""
        fish = Cuttlefish(Hat(), self.custodian)
        fish.reset()

        self.assertFalse(self.custodian.get("invert"))
        self.assertFalse(fish.invert)

        self.custodian.rotate_until("invert", True)
        # self.custodian.set("invert", True)
        fish.reconfigure()

        self.assertTrue(self.custodian.get("invert"))
        self.assertFalse(fish.invert)
