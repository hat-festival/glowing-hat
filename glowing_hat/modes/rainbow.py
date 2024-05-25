from collections import deque
from time import sleep

from glowing_hat.mode import Mode

class Rainbow(Mode):
    """Colours sliding."""

    def configure(self):
        """Configure ourself."""
        self.hues_length = len(self.hat) * self.conf["length-multiplier"]
        self.hues = deque([(x / self.hues_length) for x in range(self.hues_length)])
        self.hat.sort(self.conf["axis"])
        self.hat.apply_value(1.0)

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            for index, pixel in enumerate(self.hat.pixels):
                pixel["hue"] = self.hues[index]

            self.hat.light_up()
            sleep(self.conf["pause-time"])
            self.hues.rotate()
