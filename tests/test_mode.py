from unittest import TestCase

import pytest

from lib.conf import conf
from lib.custodian import Custodian
from lib.hat import Hat
from lib.modes.cuttlefish import Cuttlefish


class TestFish(TestCase):
    """Test the Cuttlefish."""

    def setUp(self):  # noqa: D102
        self.custodian = Custodian(namespace="test", conf=conf)
        self.custodian.populate(flush=True)

    @pytest.mark.skip(reason="breaking modes")
    def test_data(self):
        """Test it gets the correct inherited data."""
        fish = Cuttlefish(Hat(), self.custodian)

        self.assertEqual(fish.name, "cuttlefish")  # noqa: PT009
        self.assertEqual(  # noqa: PT009
            fish.data,
            {
                "fft": True,
                "jump": 1,
                "prefs": {"axis": "y", "invert": False},
                "steps": 200,
                "axis-rotate-at": 3,
            },
        )
        self.assertEqual(fish.prefs, {"axis": "y", "invert": False})  # noqa: PT009

    @pytest.mark.skip(reason="breaking modes")
    def test_resetting(self):
        """Test it resets correctly."""
        fish = Cuttlefish(Hat(), self.custodian)
        fish.reset()

        self.assertFalse(self.custodian.get("invert"))  # noqa: PT009
        self.assertFalse(fish.invert)  # noqa: PT009

        self.assertEqual(self.custodian.get("axis"), "y")  # noqa: PT009
        self.assertEqual(fish.axis, "y")  # noqa: PT009

        self.assertEqual(self.custodian.get("colour-source"), "none")  # noqa: PT009

    @pytest.mark.skip(reason="breaking modes")
    def test_reconfiguring(self):
        """Test it reconfigures correctly."""
        fish = Cuttlefish(Hat(), self.custodian)
        fish.reset()

        assert not self.custodian.get("invert")
        assert not fish.invert

        self.custodian.rotate_until("invert", True)  # noqa: FBT003
        # self.custodian.set("invert", True)
        fish.reconfigure()

        assert self.custodian.get("invert")
        assert not fish.invert
