from collections import deque
from pathlib import Path
from time import sleep

import yaml

from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource
from glowing_hat.mode import Mode


class Words(Mode):
    """Write some words."""

    def configure(self):
        """Configure."""
        self.words = yaml.safe_load(
            Path("conf", "panel", "strings", f"{self.conf['string']}.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.words = list(map(deque, self.words))

        self.hat.sort_plain()
        self.hue_source = TimeBasedHueSource(self.conf["hue-change-speed"])

    def run(self):
        """Do stuff."""
        self.configure()

        first_run = True
        while True:
            flipped = False
            self.hat.apply_hue(self.hue_source.hue())
            for index, row in enumerate(self.words):
                for i in range(32):
                    row_index = i
                    if flipped:
                        row_index = 31 - row_index
                    # self.hat.pixels[i + (32 * index)]["value"] = row[row_index]
                    self.hat.pixels[i + (32 * index)]["value"] = min(
                        1, row[row_index] + 0.3
                    )
                    self.hat.pixels[i + (32 * index)]["hue"] = (
                        self.hue_source.hue() + (row[row_index] / 2)
                    ) % 1
                flipped = not flipped
                row.rotate(-1)
            self.hat.light_up()
            sleep(self.conf["delay"])

            if first_run:
                sleep(1)
            first_run = False
