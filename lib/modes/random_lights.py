from random import random

from lib.mode import Mode
from lib.tools import hue_to_rgb


class RandomLights(Mode):
    """Random lights mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat, "Headache")

    def run(self):
        """Do stuff."""
        self.hat.off()
        while True:
            for i in range(len(self.hat)):
                self.hat.light_one(i, hue_to_rgb(random()))
            self.hat.show()
