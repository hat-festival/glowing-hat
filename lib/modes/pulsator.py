from collections import deque
from math import cos, pi
from random import randint, random

from lib.mode import Mode
from lib.tools import scale_colour


class Pulsator(Mode):
    """A huge pulsating brain."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.steps = self.data["steps"]
        self.throbbers = []

        for _ in range(len(self.hat)):
            self.throbbers.append(
                Throbber(random(), randint(self.steps["min"], self.steps["max"]))
            )

    def run(self):
        """Do the stuff."""
        while True:
            colour = self.get_colour()
            for index, throbber in enumerate(self.throbbers):
                self.hat.light_one(
                    index, scale_colour(colour, throbber.next()), auto_show=False
                )
            self.hat.show()


class Throbber(deque):
    """Cos renderer."""

    def __init__(self, seed, steps):
        """Construct."""
        self.seed = seed
        self.steps = steps

        self.populate()

    def populate(self):
        """Fill ourselves in."""
        accumulator = -1 + self.seed
        interval = (1 / self.steps) * 2

        while accumulator < 1 + self.seed:
            actual = cos(accumulator * pi)
            offset = actual + 1
            normalised = offset / 2
            rounded = round(normalised, 3)
            self.append(rounded)
            accumulator += interval

    def next(self):
        """Get the next value."""
        value = self[0]
        self.rotate(-1)

        return value
