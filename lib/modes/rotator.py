from fileinput import close
from math import cos, radians, sin

from lib.mode import Mode
from lib.tools import close_enough


class Rotator(Mode):
    """Rotator mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat, "rotator")

    def run(self):
        """Do the work."""
        while True:
            for data in generator():
                colour = self.redisman.get_colour()
                indeces = []
                for pair in data:
                    for pixel in self.hat:
                        if close_enough(pixel["x"], pair[0]):
                            if close_enough(pixel["z"], pair[1]):
                                indeces.append(pixel["index"])

                self.hat.colour_indeces(indeces, colour)


def generator():
    """Iterator."""
    for angle in range(0, 360, 15):
        yield line(angle, 8)


def line(angle, resolution=100):
    """A line for an angle as a series of pairs of points."""
    res = resolution - 1
    line = []

    for i in range(res):
        factor = i / res
        line.append((cos(radians(angle)) * factor, sin(radians(angle)) * factor))

    line.append((cos(radians(angle)), sin(radians(angle))))

    return line
