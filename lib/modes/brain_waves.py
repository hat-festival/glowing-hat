from collections import deque
from colorsys import hsv_to_rgb

from lib.mode import Mode


class BrainWaves(Mode):
    """White bands rising."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.jump = self.data["jump"]
        if self.invert:
            self.jump = 0 - self.jump

        self.steps = self.data["steps"]

        self.colours = deque()
        for i in range(self.steps):
            rgb = hsv_to_rgb(0, 0, i / self.steps)
            self.colours.append(list(map(lambda x: x * 255, rgb)))

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
