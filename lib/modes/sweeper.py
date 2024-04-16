import pickle
import random
from collections import deque
from pathlib import Path

from lib.mode import Mode

# TODO: blips as rotating list
# make it a `set`, blips maintain state, leave the set after `exit`


class Sweeper(Mode):
    """Sweeper mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        # we have this here to make it testable
        self.max_laps = None

        self.high_value = 0.9
        self.low_value = 0.1

        self.frames = pickle.loads(  # noqa: S301
            Path("renders", "radar.pickle").read_bytes()
        )

        self.lap_types = deque(
            [
                {"name": "blank", "show-blip": False, "side-effect": self.move_blip},
                {"name": "entry", "show-blip": False},
                {"name": "regular", "show-blip": True, "condition": self.should_move},
                {"name": "exit", "show-blip": True},
            ]
        )
        self.lap_type = self.lap_types[0]

    def run(self):
        """Do the work."""
        self.show_blip = False
        laps = 0

        while True:
            for count, values in enumerate(self.frames):
                if count % self.conf["jump"] == 0:
                    self.make_frame(values)

            if self.max_laps:
                laps += 1

                if laps == self.max_laps:
                    break

            self.next_lap_type()

    def make_frame(self, values):
        """Make one frame."""
        self.hat.apply_values(values)
        self.hat.apply_hue(self.conf["hues"]["main"])

        if self.reveal_on_entry(values):
            self.show_blip = True

        if self.hide_on_exit(values):
            self.show_blip = False

        if self.show_blip:
            self.hat.pixels[self.blip_index]["hue"] = self.conf["hues"]["blip"]

        self.hat.light_up()

    def reveal_on_entry(self, values):
        """Determine when to reveal the blip on an `entry` lap."""
        return (
            self.lap_type["name"] == "entry"
            and values[self.blip_index] > self.high_value
        )

    def hide_on_exit(self, values):
        """Determine when to hide the blip on an `exit` lap."""
        return (
            self.lap_type["name"] == "exit" and values[self.blip_index] < self.low_value
        )

    def next_lap_type(self):
        """Determine the next `lap_type`."""
        condition = self.lap_type.get("condition", True)
        side_effect = self.lap_type.get("side-effect", None)

        if condition:
            self.lap_types.rotate(-1)
            self.lap_type = self.lap_types[0]

        if side_effect:
            side_effect()

    def should_move(self):
        """Determine if we should move the blip."""
        return random.random() > self.conf["blip-move-threshold"]  # noqa: S311

    def move_blip(self):
        """Move the blip elsewhere."""
        self.blip_index = random.randint(0, len(self.hat) - 1)  # noqa: S311
