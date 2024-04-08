from math import radians, sin
from time import sleep

from lib.hue_sources.time_based_hue_source import TimeBasedHueSource as HueSource
from lib.mode import Mode


class Breather(Mode):
    """Breathe."""

    def configure(self):
        """Configure."""
        self.source = HueSource()

    def run(self):
        """Do the work."""
        self.configure()

        while True:
            hue = self.source.hue()
            self.breathe(less_than, hue, "-")
            self.breathe(greater_than, hue, "-")

            self.breathe(greater_than, hue)
            self.breathe(less_than, hue)

            sleep(self.conf["pause-time"])

    def breathe(self, method, hue, direction="+"):
        """Take a breath."""
        angle_offset = 90 if direction == "+" else -90

        for angle in range(0, 180, self.conf["step"]):
            sin = normalised_sin(angle + angle_offset)
            for pixel in self.hat.pixels:
                if method(pixel["y"], sin):
                    pixel["value"] = 1.0
                    pixel["hue"] = hue
                else:
                    pixel["value"] = self.conf["scale-factor"]

            self.hat.light_up()


def greater_than(this, that):
    """Greater than."""
    return this > that


def less_than(this, that):
    """Greater than."""
    return this < that


def normalised_sin(angle):
    """`sin` between 0 and 1."""
    return (sin(radians(angle)) + 1) / 2
