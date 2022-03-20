from random import random

from lib.mode import Mode
from lib.tools import hue_to_rgb


class Headache(Mode):
    """Random lights mode."""

    def run(self):
        """Do stuff."""
        while True:
            for i in range(len(self.hat)):
                self.hat.light_one(i, hue_to_rgb(random()))
            self.hat.show()
