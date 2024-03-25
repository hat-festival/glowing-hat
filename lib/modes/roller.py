from collections import deque
from time import sleep

from lib.arrangements.circle import Circle
from lib.fft_pool import FFTPool
from lib.logger import logging
from lib.mode import Mode
from lib.tools import hue_to_rgb, scale_colour


class Roller(Mode):
    """Subtly rolling."""

    def configure(self):
        """Configure ourself."""
        self.decay_amount = self.data["decay"]["amount"]
        self.decay_interval = self.data["decay"]["interval"]

        self.max_brightness = self.data["brightness"]["max"]
        self.default_brightness = self.data["brightness"]["default"]
        self.brightness_factor = self.default_brightness

        self.fft_pool = FFTPool(self)

        self.rotate_amount = self.data["rotate-amount"]
        self.hues_length = len(self.hat) * self.data["length-multiplier"]
        self.hues = deque([(x / self.hues_length) for x in range(self.hues_length)])
        self.circle = Circle(self.hat, "x", "z")

    def run(self):
        """Do the work."""
        self.configure()

        count = 0
        indeces = []
        while True:
            # if count % self.data["roll-sorter-at"] == 0:
            #     indeces = self.circle.next()
            #     count = 0


            # for pixel in enumerate(self.hat.pixels):
            #     pixel["hue"] = self.hues[index]
            #     pixel["value"] = self.brightness_factor


            self.hat.light_up()


            self.hues.rotate(self.rotate_amount)
            count += 1

    def trigger(self):
        """We are triggered."""
        self.brightness_factor = self.max_brightness

    def reduce(self):
        """Constantly reducing the brightness."""
        while True:
            if self.brightness_factor > self.default_brightness:
                self.brightness_factor -= self.decay_amount
                sleep(self.decay_interval)
