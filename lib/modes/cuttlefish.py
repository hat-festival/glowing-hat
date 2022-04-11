from collections import deque

from lib.mode import Mode
from lib.tools import hue_to_rgb


class Cuttlefish(Mode):
    """Ripples of colour."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.jump = self.data["jump"]
        if self.invert:
            self.jump = 0 - self.jump

        self.steps = self.data["steps"]

        self.colours = deque()
        for i in range(self.steps):
            self.colours.append(hue_to_rgb(i / self.steps))

        self.hat.sort(self.axis)

    def run(self):
        """Do the stuff."""
        while True:
            self.hat.illuminate(list(self.colours)[:100])
            self.colours.rotate(self.jump)
