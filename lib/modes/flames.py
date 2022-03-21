from random import random

from lib.mode import Mode
from lib.tools import hue_to_rgb


class Flames(Mode):
    """Flames."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.hat.sort(key=lambda w: w[self.axis])
        self.hat.reverse()

    def run(self):
        """Do the stuff."""
        while True:
            for index in range(len(self.hat) - 1, 0, -1):
                light = self.hat[index]
                weight = index / 100

                colour = hue_to_rgb(weight * 0.3 * random())

                self.hat.light_one(light["index"], colour)
