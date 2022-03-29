from collections import deque

from lib.mode import Mode
from lib.tools import scale_colour

# from colorsys import hsv_to_rgb
# from time import sleep


class ColourBrain(Mode):
    """Colours."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.hat.sort(key=lambda w: w[self.axis])

        self.jump = self.conf["modes"]["colour-brain"]["jump"]
        if self.invert:
            self.jump = 0 - self.jump

        self.steps = self.conf["modes"]["colour-brain"]["steps"]

        self.values = deque()
        for i in range(self.steps):
            self.values.append(i / self.steps)

        for _ in range(100):
            self.values.append(0)

    def run(self):
        """Do the stuff."""
        while True:

            self.values = deque()
            for _ in range(100):
                self.values.append(0)
            for i in range(self.steps):
                self.values.append(i / self.steps)
            for _ in range(10):
                self.values.append(1)
            for _ in range(10):
                self.values.append(0)

            count = 0
            while count < 30:
                colour = self.custodian.get("colour")
                for i, _ in enumerate(self.hat):
                    self.hat.light_one(
                        self.hat[i]["index"],
                        scale_colour(colour, self.values[i]),
                        auto_show=False,
                    )
                count += 1
                self.hat.show()
                self.values.rotate(self.jump)

            self.hat.reverse()
            # sleep(self.conf["modes"]["colour-brain"]["delay"])
