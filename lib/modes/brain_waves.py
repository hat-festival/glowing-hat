import pickle
from collections import deque

from lib.axis_rotator import random_step
from lib.logger import logging
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
            self.values.reverse()

        self.sort_hat()
        self.sorts_key = "sorts:(1.0, 1.0, 1.0)"

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        count = 0
        while True:
            self.hat.pixels = pickle.loads(self.redis.get(self.sorts_key))  # noqa: S301
            clr = self.get_colour()
            rgbs = list(  # noqa: C417
                map(lambda x: scale_colour(clr, x), list(self.values)[:100])
            )
            self.hat.illuminate(rgbs)
            self.values.rotate(self.jump)

            count += 1
            if count == len(self.values) / 2:
                self.sorts_key = random_step(self.sorts_key)
                logging.debug(self.sorts_key)
                count = 0
