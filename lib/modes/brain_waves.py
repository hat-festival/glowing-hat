from collections import deque

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
        for i in range(self.steps):
            self.values.append(i / self.steps)

    def reconfigure(self):
        """Configure ourself."""
        if self.invert:
            self.jump = 0 - self.jump

        self.sort_hat()

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        while True:
            # clr = [255, 255, 255]
            clr = self.get_colour()
            rgbs = list(map(lambda x: scale_colour(clr, x), list(self.values)[:100]))
            self.hat.illuminate(rgbs)
            self.values.rotate(self.jump)
