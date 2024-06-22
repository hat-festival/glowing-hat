from collections import deque
from time import sleep

from glowing_hat.arrangements.circle import Circle
from glowing_hat.mode import Mode
from glowing_hat.tempo.tempo_pool import TempoPool


class Roller(Mode):
    """Subtly rolling."""

    def configure(self):
        """Configure ourself."""
        self.hues_length = len(self.hat) * self.conf["length-multiplier"]
        self.hues = deque([(x / self.hues_length) for x in range(self.hues_length)])
        self.circle = Circle("x", "z")

        self.brightness_factor = self.conf["brightness"]["default"]
        self.tempo_pool = TempoPool(self)

    def run(self):
        """Do the work."""
        self.configure()

        count = 0
        while True:
            if count % self.conf["roll-sorter-at"] == 0:
                self.hat.sort_by_indeces(self.circle.next())
                count = 0

            self.hat.apply_hues(self.hues)
            self.hat.apply_value(self.brightness_factor)

            self.hat.light_up()

            self.hues.rotate(self.conf["rotate-amount"])
            count += 1

    def trigger(self):
        """We are triggered."""
        self.brightness_factor = self.conf["brightness"]["max"]

    def reduce(self):
        """Constantly reducing the brightness."""
        while True:
            if self.brightness_factor > self.conf["brightness"]["default"]:
                self.brightness_factor -= self.conf["decay"]["amount"]
                sleep(self.conf["decay"]["interval"])
