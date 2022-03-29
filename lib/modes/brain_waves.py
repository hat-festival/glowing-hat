from collections import deque
from colorsys import hsv_to_rgb

from lib.mode import Mode


class BrainWaves(Mode):
    """White bands rising."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.hat.sort(key=lambda w: w[self.axis])

        self.jump = self.conf["modes"]["brain-waves"]["jump"]
        if self.invert:
            self.jump = 0 - self.jump

        self.steps = self.conf["modes"]["brain-waves"]["steps"]

        self.colours = deque()
        for i in range(self.steps):
            rgb = hsv_to_rgb(0, 0, i / self.steps)
            self.colours.append(list(map(lambda x: x * 255, rgb)))

    def run(self):
        """Do the stuff."""
        while True:
            for i, _ in enumerate(self.hat):
                self.hat.light_one(
                    self.hat[i]["index"], self.colours[i], auto_show=False
                )
            self.hat.show()
            self.colours.rotate(self.jump)
