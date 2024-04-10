import pickle
import random
from pathlib import Path

from lib.mode import Mode

# TODO: have a wandering axis_manager spot?


class Sweeper(Mode):
    """Sweeper mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)
        self.max_laps = None

    def configure(self):
        """Configure ourself."""
        self.frames = pickle.loads(  # noqa: S301
            Path("renders", "radar.pickle").read_bytes()
        )
        self.blip_index = None
        self.fixtures = []

    def run(self):  # noqa: C901, PLR0912
        """Do the work."""
        self.configure()

        lap_type = "blank"
        show_blip = False
        laps = 0

        while True:
            if lap_type in ("regular", "exit"):
                show_blip = True
            if lap_type in ("blank", "entry"):
                show_blip = False

            for count, values in enumerate(self.frames):
                if count % self.conf["jump"] == 0:
                    self.hat.apply_values(values)
                    self.hat.apply_hue(self.conf["hues"]["main"])

                    if self.blip_index:
                        if lap_type == "entry" and values[self.blip_index] > 0.9:  # noqa: PLR2004
                            show_blip = True

                        if show_blip:
                            self.hat.pixels[self.blip_index]["hue"] = self.conf["hues"][
                                "blip"
                            ]

                        if lap_type == "exit" and values[self.blip_index] < 0.1:  # noqa: PLR2004
                            show_blip = False

                    self.hat.light_up()
                    self.fixtures.append(list(self.hat.lights))

            if self.max_laps:
                laps += 1

                if laps == self.max_laps:
                    break

            if lap_type == "entry":
                lap_type = "regular"

            elif (
                lap_type == "regular"
                and random.random() > self.conf["blip-move-threshold"]  # noqa: S311
            ):
                lap_type = "exit"

            elif lap_type == "exit":
                lap_type = "blank"

            elif lap_type == "blank":
                self.blip_index = random.randint(0, 99)  # noqa: S311
                lap_type = "entry"
