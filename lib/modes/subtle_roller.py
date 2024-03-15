from collections import deque

from lib.arrangements.circle import Circle
from lib.mode import Mode
from lib.tools import hue_to_rgb


class SubtleRoller(Mode):
    """Subtly rolling."""

    def configure(self):
        """Configure ourself."""
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
            self.from_list(self.lights)
            self.lights.rotate(self.rotate_amount)
            count += 1
