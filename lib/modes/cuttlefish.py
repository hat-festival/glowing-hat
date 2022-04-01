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

    def run(self):
        """Do the stuff."""
        self.sort_hat()

        while True:
            for i, _ in enumerate(self.hat):
                self.hat.light_one(
                    self.hat[i]["index"], self.colours[i], auto_show=False
                )

            self.hat.show()
            self.colours.rotate(self.jump)
