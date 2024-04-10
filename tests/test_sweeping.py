# randint = 33
# random = 1.0
from unittest.mock import patch  # noqa: I001
import random
import json
from pathlib import Path

from lib.hat import Hat
from lib.modes.sweeper import Sweeper


def test_sweeping():
    """Test it sweeps."""
    raw_fixture = json.loads(
        Path("tests/fixtures/sweeper/lights.json").read_text(encoding="utf-8")
    )
    fixture = []
    for item in raw_fixture:
        fixture.append([tuple(x) for x in item])  # noqa: PERF401

    with patch.object(random, "randint", return_value=33):  # noqa: SIM117
        with patch.object(random, "random", return_value=1.0):
            hat = Hat()
            hat.brightness_control.factor.value = 0.5
            swp = Sweeper(hat)
            swp.max_laps = 6
            swp.run()

            assert hat.lights.record == fixture
