from random import random

from lib.pixel_hat import PixelHat
from lib.tools import hue_to_rgb


class Random:
    """Random lights mode."""

    ### Make a superclass that parses a conf-file for settings?
    def __init__(self, hat):
        """Construct."""
        self.hat = hat

    def run(self):
        """Do stuff."""
        self.hat.off()
        while True:
            lights = []
            for i in range(len(self.hat)):
                self.hat.light_one(i, hue_to_rgb(random()))
            self.hat.show()
