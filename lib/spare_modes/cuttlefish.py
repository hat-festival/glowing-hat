from collections import deque

from lib.arrangements.circle import Circle
from lib.mode import Mode
from lib.tools.utils import hue_to_rgb


class Cuttlefish(Mode):
    """Ripples of colour."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)
        self.jump = self.conf["jump"]
        self.steps = self.conf["steps"]
        self.colours = deque()
        self.circle = Circle(self.hat, "x", "z")
        for i in range(self.steps):
            self.colours.append(hue_to_rgb(i / self.steps))

    def reconfigure(self):
        """Configure ourself."""
        if self.invert:
            self.jump = 0 - self.jump

    def run(self):
        """Do the stuff."""
        self.reconfigure()
        self.circle.next()

        count = 0
        while True:
            self.hat.illuminate(list(self.colours)[: self.hat.length])
            self.colours.rotate(self.jump)

            count += 1
            if count == self.conf["axis-rotate-at"]:
                self.circle.next()
                count = 0
