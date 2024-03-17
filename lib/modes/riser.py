from random import random

from lib.mode import Mode


class Riser(Mode):
    """Rise up."""

    def reconfigure(self):
        """Configure ourself."""
        self.primary = [255, 0, 0]
        self.secondary = [0, 0, 255]
        self.sort_hat("y")

    def run(self):
        """Do the stuff."""
        self.reconfigure()
        while True:
            lights = []
            for i in range(len(self.hat)):
                if random() > i / len(self.hat):  # noqa: S311
                    lights.append(self.primary)
                else:
                    lights.append(self.secondary)

                self.from_list(lights)
