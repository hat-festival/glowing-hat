from collections import deque
from pathlib import Path
from time import sleep

import yaml

from glowing_hat.hue_sources.random_hue_source import RandomHueSource
from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource
from glowing_hat.mode import Mode
from glowing_hat.tools.sin_looper import SinLooper


class Invaders(Mode):
    """Space Invaders."""

    def configure(self):
        """Configure."""
        self.ambient_hue_source = TimeBasedHueSource(self.conf["hue-change-speed"])
        self.alien_hue_source = RandomHueSource()
        self.base_hue = self.alien_hue_source.hue()
        self.data = yaml.safe_load(
            Path("conf", "panel", "invaders.yaml").read_text(encoding="utf-8")
        )
        self.hat.sort("x")
        self.timer = SinLooper(
            self.conf["interval"]["low"],
            self.conf["interval"]["high"],
            self.conf["interval"]["steps"],
        )

        self.sets = {
            "left": deque([]),
            "right": deque([]),
        }

        self.make_aliens()
        self.insert_alien(self.data["saucer"], hue=self.base_hue)
        self.rotate_hue()

    def make_aliens(self):
        """Make the aliens."""
        aliens = self.data["aliens"]
        for _ in range(self.conf["invader-count"]):
            for invader in aliens:
                self.insert_alien(aliens[invader], hue=self.base_hue)
                flip_variants(aliens[invader])
                self.rotate_hue()

    def rotate_hue(self):
        """Rotate the base hue."""
        self.base_hue += float(self.conf["hue-gap"])

    def insert_alien(self, data, hue=1.0):
        """Append us some data."""
        for variant in self.sets:
            self.sets[variant] += self.create_frame(data[variant], data["width"], hue)

            for _ in range(self.conf["gap"]):
                self.sets[variant].append([0] * 8)

    def create_frame(self, data, width, hue):
        """Create a frame."""
        return [self.create_bar(bar, hue) for bar in self.create_bits(data, width)]

    def create_bar(self, bar, hue):
        """Make a bar."""
        return tuple(int(x) * hue for x in reversed(bar))

    def create_bits(self, data, width):
        """Make them bits."""
        bits = [list(f"{x:0{width}b}") for x in data]
        return zip(*bits[::-1], strict=False)

    def run(self):
        """Do stuff."""
        self.configure()
        self.hat.off()

        self.sets["right"].rotate(-1)

        count = 0
        while True:
            for variant in self.sets:
                hue = self.ambient_hue_source.hue()
                background_hue = self.ambient_hue_source.inverse_hue()
                self.hat.apply_hue(background_hue)
                self.hat.apply_value(self.conf["inverse-value"])

                for outer_index, bar in enumerate(self.sets[variant]):
                    if outer_index < 32:  # noqa: PLR2004
                        for index, bit in enumerate(bar):
                            pixel = self.hat.pixels[index + (8 * outer_index)]
                            if bit > 0:
                                pixel["value"] = 1
                                pixel["hue"] = (bit + hue) % 1

                    count += 1

                self.hat.light_up()
                self.sets[variant].rotate(-2)
                # sleep(self.conf["interval"])
                sleep(next(self.timer))


def flip_variants(alien):
    """Flip them frames."""
    tmp = alien["left"]
    alien["left"] = alien["right"]
    alien["right"] = tmp
