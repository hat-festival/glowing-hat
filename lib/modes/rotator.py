from fileinput import close
from math import radians, sin, cos

from lib.mode import Mode
from lib.tools import close_enough


class Rotator(Mode):
    """Rotator mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat, "rotator")

    def run(self):
        """Do the work."""
        # for w in range(360):
        #     print(sin(radians(w)))

        self.hat.off()
        indeces = []
        for pixel in self.hat:
            # if close_enough(pixel["z"], 0):
            #     indeces.append(pixel["index"])
            for w in range(100):
                v = w / 100
                if close_enough(pixel["x"], v):
                    if close_enough(pixel["z"], 0 - pixel["x"]):
                        indeces.append(pixel["index"])

        self.hat.colour_indeces(indeces, [0, 255, 0])


def generator():
    """Iterator."""
    for w in range(360):
        print(sin(radians(w)))


def line(angle, resolution=100):
    """A line for an angle as a series of pairs of points."""
    line = [(0.0, 0.0)]

    next_hop = (
        cos(radians(angle)),
        sin(radians(angle)) 
    )

    line.append(next_hop)

    return line
