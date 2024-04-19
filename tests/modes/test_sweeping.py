import json
import platform
import random
from pathlib import Path
from unittest.mock import patch

from glowing_hat.hat import Hat
from glowing_hat.modes.sweeper import Sweeper


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
            with patch.object(platform, "node", return_value="glowing-hat"):
                hat = Hat()
                hat.brightness_control.factor.value = 0.5
                swp = Sweeper(hat)
                swp.max_laps = 6

                swp.conf["hues"] = {}
                swp.conf["hues"]["blip"] = 1.0
                swp.conf["hues"]["main"] = 0.333333
                swp.conf["jump"] = 4

                swp.run()

                assert hat.lights.record == fixture
