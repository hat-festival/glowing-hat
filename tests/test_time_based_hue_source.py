# @patch("lib.arrangements.riser_list.random")
from unittest.mock import patch  # noqa: I001
import time

from lib.hue_sources.time_based_hue_source import TimeBasedHueSource


def test_one_per():
    """Test when it's one rotation per second."""
    tbhs = TimeBasedHueSource(seconds_per_rotation=1)

    with patch.object(time, "time", return_value=1.000000):
        assert tbhs.hue() == 0.0

    with patch.object(time, "time", return_value=431.75):
        assert tbhs.hue() == 0.75  # noqa: PLR2004


def test_two_per():
    """Test when it's two seconds per rotation."""
    tbhs = TimeBasedHueSource(seconds_per_rotation=2)

    with patch.object(time, "time", return_value=0.000000):
        assert tbhs.hue() == 0.0

    with patch.object(time, "time", return_value=0.500000):
        assert tbhs.hue() == 0.25  # noqa: PLR2004

    with patch.object(time, "time", return_value=1.000000):
        assert tbhs.hue() == 0.5  # noqa: PLR2004

    with patch.object(time, "time", return_value=1.500000):
        assert tbhs.hue() == 0.75  # noqa: PLR2004


def test_three_per():
    """Test when it's three seconds per rotation."""
    tbhs = TimeBasedHueSource(seconds_per_rotation=3)

    with patch.object(time, "time", return_value=0.000000):
        assert tbhs.hue() == 0.0

    with patch.object(time, "time", return_value=1.500000):
        assert tbhs.hue() == 0.5  # noqa: PLR2004

    with patch.object(time, "time", return_value=3.500000):
        assert tbhs.hue() == 1 / 6


def test_five_per():
    """Test when it's five seconds per rotation."""
    tbhs = TimeBasedHueSource(seconds_per_rotation=5)

    with patch.object(time, "time", return_value=0.000000):
        assert tbhs.hue() == 0.0

    with patch.object(time, "time", return_value=2.500000):
        assert tbhs.hue() == 0.5  # noqa: PLR2004


def test_fractional_per():
    """Test it works with fractional seconds per rotation."""
    tbhs = TimeBasedHueSource(seconds_per_rotation=2.5)
    with patch.object(time, "time", return_value=0.000000):
        assert tbhs.hue() == 0.0

    with patch.object(time, "time", return_value=1.500000):
        assert tbhs.hue() == 0.6  # noqa: PLR2004

    with patch.object(time, "time", return_value=2.500000):
        assert tbhs.hue() == 0.0
