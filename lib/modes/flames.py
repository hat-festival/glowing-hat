from random import random
from time import sleep

from lib.mode import Mode
from lib.tools import hue_to_rgb


class Flames(Mode):
    """Flames."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.hat.sort(key=lambda w: w[self.axis])

    def run(self):
        """Do the stuff."""
        yellow = 0.2
        values = []
        limit = 80
        modifier = 0.05
        margin = 0.2

        for _ in range(100 - limit):
            values.append(yellow)

        for i in range(limit):
            weight = (limit - i) / limit
            values.append(weight * yellow)

        while True:
            for i, _ in enumerate(self.hat):
                value = values[i]
                dice = random()
                if dice > (1 - margin):
                    value += modifier
                    value = min(value, yellow)
                if dice < margin:
                    value -= modifier
                    value = max(value, 0)

                colour = hue_to_rgb(value)
                self.hat.light_one(self.hat[i]["index"], colour)
                sleep(0.01)
