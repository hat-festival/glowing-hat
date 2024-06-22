from collections import deque
from math import pi, sin
from operator import itemgetter
from random import randint
from time import sleep

from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource
from glowing_hat.mode import Mode
from glowing_hat.tempo.tempo_pool import TempoPool


class Pulsator(Mode):
    """A huge pulsating brain."""

    def configure(self):
        """Reconfig some stuff."""
        self.hue_source = TimeBasedHueSource(
            seconds_per_rotation=self.conf["hue-seconds-per-rotation"]
        )
        self.throbbers = [Throbber(self.conf["steps"]) for _ in range(len(self.hat))]
        self.value_multiplier = self.conf["base-value"]
        self.saturation = 1.0
        self.tempo_pool = TempoPool(self)

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            hue = self.hue_source.hue()
            self.hat.apply_saturation(self.saturation)
            self.hat.apply_hue(hue)
            self.hat.apply_values(
                [throbber.next() * self.value_multiplier for throbber in self.throbbers]
            )

            self.hat.light_up()

    def trigger(self):
        """Spike the saturation."""
        self.value_multiplier = 1.0
        self.saturation = 0.0

    def reduce(self):
        """Constantly resaturating."""
        while True:
            if self.value_multiplier > self.conf["base-value"]:
                self.value_multiplier -= self.conf["decay"]["amount"]
            if self.saturation < 1.0:
                self.saturation += self.conf["decay"]["amount"]
            sleep(self.conf["decay"]["interval"])


class Throbber:
    """Sin renderer."""

    def __init__(self, minmax):
        """Construct."""
        self.values = deque()
        self.min, self.max = itemgetter("min", "max")(minmax)

    def next(self):
        """Get the next value."""
        if len(self.values) == 0:
            self.refresh()

        value = self.values.popleft()
        return value  # noqa: RET504

    def refresh(self):
        """Generate a sin-curve."""
        self.values = deque([])
        accumulator = -1
        interval = (1 / randint(self.min, self.max)) * 2  # noqa: S311

        while accumulator < 1:
            actual = sin(accumulator * pi)
            offset = actual + 1
            normalised = offset / 2
            rounded = round(normalised, 3)
            self.values.append(rounded)
            accumulator += interval
