from collections import deque
from pathlib import Path
from time import sleep

import yaml

from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource
from glowing_hat.mode import Mode


class Invaders(Mode):
    """Space Invaders."""

    def configure(self):
        """Configure."""
        self.hue_source = TimeBasedHueSource(self.conf["hue-change-speed"])
        self.data = yaml.safe_load(
            Path("conf", "panel", "invaders.yaml").read_text(encoding="utf-8")
        )
        self.hat.sort("x")
        self.invaders = deque(self.data.keys())
        self.variants = deque(["first", "second"])

    def run(self):
        """Do stuff."""
        self.configure()
        self.hat.off()

        count = 0

        while True:
            invader = self.invaders[0]
            variant = self.variants[0]
            offset = int((32 - self.data[invader]["width"]) / 2)

            hue = self.hue_source.hue()
            self.hat.apply_hue(self.hue_source.inverse_hue())
            self.hat.apply_value(self.conf["inverse-value"])

            for z_index, value in enumerate(self.data[invader][variant]):
                bits = f"{value:0{self.data[invader]['width']}b}"
                for index, bit in enumerate(bits):
                    pixel = self.hat.pixels[z_index + (8 * index) + (8 * offset)]
                    if int(bit) == 1:
                        pixel["value"] = 1
                        pixel["hue"] = hue

            self.hat.light_up()
            self.variants.rotate()
            sleep(self.conf["interval"])

            count += 1
            if count == self.conf["iterations"]:
                self.hat.apply_hue(self.hue_source.inverse_hue())
                self.hat.apply_value(self.conf["inverse-value"])
                self.hat.light_up()
                sleep(self.conf["interval"])

                hue = self.hue_source.hue()
                self.invaders.rotate()
                count = 0
