from collections import deque
from time import sleep

from lib.mode import Mode


class Rainbow(Mode):
    """Colours sliding."""

    def configure(self):
        """Configure ourself."""
        self.hues_length = len(self.hat) * self.conf["length-multiplier"]
        self.hues = deque([(x / self.hues_length) for x in range(self.hues_length)])
        self.hat.sort(self.conf["axis"])

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            for pixel in self.hat.pixels:
                pixel["hue"] = self.hues[pixel["index"]]

            self.hat.light_up()
            sleep(self.conf["pause-time"])
            self.hues.rotate()
