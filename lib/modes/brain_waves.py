from collections import deque

from lib.arrangements.circle import Circle
from lib.mode import Mode
from lib.tools import scale_colour


class BrainWaves(Mode):
    """White bands rising."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)
        self.jump = self.data["jump"]
        self.steps = self.data["steps"]
        self.values = deque()
        self.circle = Circle(self.hat, "z", "y", "x")
        for i in range(self.steps):
            self.values.append(i / self.steps)

    def reconfigure(self):
        """Configure ourself."""
        if self.invert:
            self.jump = 0 - self.jump
            self.values.reverse()

        # self.sort_hat()
        self.circle.next()

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        count = 0
        while True:
            clr = self.get_colour()
            rgbs = [scale_colour(clr, x) for x in list(self.values)[:100]]
            self.hat.illuminate(rgbs)
            self.values.rotate(self.jump)
            count += 1
            if count == self.data["axis-rotate-at"]:
                self.circle.next()
                count = 0
