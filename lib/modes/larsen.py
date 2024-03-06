from collections import deque

from lib.mode import Mode
from lib.tools import scale_colour


class Larsen(Mode):
    """Larsen scanner."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)
        self.jump = self.data["jump"]
        self.steps = self.data["steps"]
        self.values = deque()

        for i in range(self.steps):  # noqa: B007
            self.values.append(0)
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

        count = 0
        clr = self.get_colour()
        while True:
            rgbs = list(  # noqa: C417
                map(lambda x: scale_colour(clr, x), list(self.values)[: len(self.hat)])
            )
            self.hat.illuminate(rgbs)
            self.values.rotate(self.jump)

            count += self.jump
            if abs(count) >= len(self.values):
                self.hat.reverse()
                clr = self.get_colour()
                count = 0
