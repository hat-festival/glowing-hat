from random import random

from lib.tools import hue_to_rgb


class RandomLights:
    """Random lights mode."""

    ### Make a superclass that parses a conf-file for settings?
    def __init__(self, hat):
        """Construct."""
        self.name = "Headache-Inducer"
        self.hat = hat

    def run(self):
        """Do stuff."""
        self.hat.off()
        while True:
            for i in range(len(self.hat)):
                self.hat.light_one(i, hue_to_rgb(random()))
            self.hat.show()
