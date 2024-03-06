from collections import deque

from lib.arrangements.circle import Circle
from lib.mode import Mode
from lib.tools import hue_to_rgb


class SubtleRoller(Mode):
    """Subtly rolling."""

    def reconfigure(self):
        """Configure ourself."""
        self.lights_length = len(self.hat) * self.data["length-multiplier"]
        self.lights = deque(
            [hue_to_rgb(x / self.lights_length) for x in range(self.lights_length)]
        )
        self.sort_hat()
        self.circle = Circle(self.hat, "x", "z")

    def run(self):
        """Do the work."""
        self.reconfigure()

        count = 0
        while True:
            if count % self.data["roll-sorter-at"] == 0:
                self.circle.next()
            self.hat.illuminate(list(self.lights)[: len(self.hat)])
            self.lights.rotate()
            count += 1
