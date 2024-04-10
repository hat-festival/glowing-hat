import pickle
import random
from collections import deque
from pathlib import Path

from lib.mode import Mode


class Sweeper(Mode):
    """Sweeper mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)
        self.max_laps = None

        self.lap_types = deque(
            [
                {"name": "blank", "show-blip": False, "side-effect": self.move_blip},
                {"name": "entry", "show-blip": False},
                {"name": "regular", "show-blip": True, "condition": self.should_move},
                {"name": "exit", "show-blip": True},
            ]
        )

    def configure(self):
        """Configure ourself."""
        self.frames = pickle.loads(  # noqa: S301
            Path("renders", "radar.pickle").read_bytes()
        )
        self.blip_index = None
        self.lap_type = self.lap_types[0]

    def run(self):
        """Do the work."""
        self.configure()

        show_blip = False
        laps = 0

        while True:
            show_blip = self.lap_type["show-blip"]

            for count, values in enumerate(self.frames):
                if count % self.conf["jump"] == 0:
                    self.hat.apply_values(values)
                    self.hat.apply_hue(self.conf["hues"]["main"])

                    if self.blip_index:
                        if (
                            self.lap_type["name"] == "entry"
                            and values[self.blip_index] > 0.9  # noqa: PLR2004
                        ):
                            show_blip = True

                        if show_blip:
                            self.hat.pixels[self.blip_index]["hue"] = self.conf["hues"][
                                "blip"
                            ]

                        if (
                            self.lap_type["name"] == "exit"
                            and values[self.blip_index] < 0.1  # noqa: PLR2004
                        ):
                            show_blip = False

                    self.hat.light_up()

            if self.max_laps:
                laps += 1

                if laps == self.max_laps:
                    break

            self.next_lap_type()

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
        self.blip_index = random.randint(0, 99)  # noqa: S311
