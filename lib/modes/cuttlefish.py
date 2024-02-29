import pickle
from collections import deque

from lib.axis_rotator import circle
from lib.logger import logging
from lib.mode import Mode
from lib.tools import hue_to_rgb


class Cuttlefish(Mode):
    """Ripples of colour."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)
        self.jump = self.data["jump"]
        self.steps = self.data["steps"]
        self.colours = deque()
        for i in range(self.steps):
            self.colours.append(hue_to_rgb(i / self.steps))

    def reconfigure(self):
        """Configure ourself."""
        if self.invert:
            self.jump = 0 - self.jump

        self.sort_hat()
        self.axes = deque(circle(("x", "z")))

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        count = 0
        while True:
            self.hat.pixels = pickle.loads(self.redis.get(self.axes[0]))  # noqa: S301
            self.hat.illuminate(list(self.colours)[: self.hat.length])
            count += 1
            if count == 3:  # noqa: PLR2004
                logging.debug(self.axes[0])
                self.axes.rotate()
                count = 0

            self.colours.rotate(self.jump)
