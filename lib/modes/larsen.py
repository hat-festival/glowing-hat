from enum import auto
from math import ceil
from time import sleep

from lib.mode import Mode
from lib.tools import scale_colour


class Larsen(Mode):
    """Larsen scanner."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.jump = self.data["jump"]
        self.width = self.data["width"]

    def run(self):
        """Do the stuff."""
        self.sort_hat()
        self.hat.off()
        while True:
            colour = self.get_colour()
            for index, frame in enumerate(self.frame_sets):
                if index % 5 == 0:
                    colours = list(map(lambda x: scale_colour(colour, x), frame))
                    for index, value in enumerate(colours):
                        self.hat.light_one(self.hat[index]["index"], value, auto_show=False)

                    self.hat.show()

            self.hat.reverse()
