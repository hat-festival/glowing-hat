from collections import deque
from pathlib import Path
from time import sleep

import yaml

from glowing_hat.custodian import Custodian
from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource
from glowing_hat.mode import Mode


class Words(Mode):
    """Write some words."""

    def configure(self):
        """Configure."""
        self.hat.off()
        self.custodian = Custodian(conf=self.conf, namespace="hat")
        string = self.custodian.get("string")
        self.words = yaml.safe_load(
            Path("conf", "panel", "strings", f"{string}.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.words = list(map(deque, self.words))

        self.hue_source = TimeBasedHueSource(self.conf["hue-change-speed"])
        self.hat.sort_plain()

    def run(self):
        """Do stuff."""
        self.configure()

        first_run = True
        while True:
            flipped = False
            self.hat.apply_hue(self.hue_source.hue())
            for index, row in enumerate(self.words):
                offset = 32 * index
                for i in range(32):
                    row_index = i
                    if flipped:
                        row_index = 31 - row_index

                    val_hue = (1, self.hue_source.hue())
                    if row[row_index] == 0:
                        val_hue = (0.3, self.hue_source.inverse_hue())

                    pixel = self.hat.pixels[i + offset]
                    pixel["value"], pixel["hue"] = val_hue

                flipped = not flipped
                row.rotate(-1)

            self.hat.light_up()
            sleep(self.conf["delay"])

            if first_run:
                sleep(0.5)
            first_run = False
