import pickle
from pathlib import Path
from random import randint, random

from lib.mode import Mode


class Sweeper(Mode):
    """Sweeper mode."""

    def configure(self):
        """Configure ourself."""
        self.frames = pickle.loads(  # noqa: S301
            Path("renders", "radar.pickle").read_bytes()
        )
        self.blip_index = None

    def run(self):
        """Do the work."""
        self.configure()

        while True:
            count = 0
            if random() > self.conf["blip-move-threshold"]:  # noqa: S311
                self.blip_index = None

            for values in self.frames:
                if count % self.conf["jump"] == 0:
                    self.hat.apply_values(values)
                    self.hat.apply_hue(self.conf["hues"]["main"])
                    if self.blip_index:
                        self.hat.pixels[self.blip_index]["hue"] = self.conf["hues"][
                            "blip"
                        ]
                    self.hat.light_up()

                count += 1  # noqa: SIM113

            if not self.blip_index:
                self.blip_index = randint(0, 99)  # noqa: S311
