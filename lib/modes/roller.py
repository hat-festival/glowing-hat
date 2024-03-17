import concurrent.futures
from collections import deque

# from multiprocessing import Value
from time import sleep

from lib.arrangements.circle import Circle
from lib.fourier import Fourier
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

        self.fft = Fourier(self)

        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.pool.submit(self.fft.transform)
        self.pool.submit(self.reduce)

        self.rotate_amount = self.data["rotate-amount"]
        self.lights_length = len(self.hat) * self.data["length-multiplier"]
        self.hues = [(x / self.lights_length) for x in range(self.lights_length)]
        self.lights = deque([hue_to_rgb(x) for x in self.hues])
        self.circle = Circle(self.hat, "x", "z")

    def run(self):
        """Do the work."""
        self.configure()

        count = 0
        while True:
            if count % self.data["roll-sorter-at"] == 0:
                self.circle.next()
                count = 0
            self.from_list(
                [scale_colour(x, self.brightness_factor) for x in self.lights][
                    0 : len(self.hat) - 1
                ]
            )
            self.lights.rotate(self.rotate_amount)
            count += 1

    def trigger(self):
        """We are triggered."""
        logging.debug("triggering")
        self.brightness_factor = self.max_brightness

    def reduce(self):
        """Constantly reducing the brightness."""
        while True:
            if self.brightness_factor > self.default_brightness:
                self.brightness_factor -= self.decay_amount
                sleep(self.decay_interval)
        # else:
        #     sleep(1)
