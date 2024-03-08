from collections import deque

from lib.arrangements.circle import Circle
from lib.mode import Mode
from lib.tools import scale_colour


class BrainWaves(Mode):
    """Bands rising."""

    def reconfigure(self):
        """Configure ourself."""
        self.jump = self.data["jump"]
        self.steps = self.data["steps"]

        self.values = deque()
        for i in range(self.steps):
            self.values.append(i / self.steps)

        self.circle = Circle(self.hat, "z", "x")
        self.circle.next()

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        count = 0
        while True:
            clr = self.get_colour()
            rgbs = [scale_colour(clr, x) for x in list(self.values)[: len(self.hat)]]
            self.hat.illuminate(rgbs)
            self.values.rotate(self.jump)
            count += 1
            if count == self.data["axis-rotate-at"]:
                self.circle.next()
                count = 0
