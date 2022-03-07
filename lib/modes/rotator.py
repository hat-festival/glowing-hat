from math import cos, radians, sin

from lib.mode import Mode
from lib.tools import close_enough, scale_colour


class Rotator(Mode):
    """Rotator mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat, "rotator")

    def run(self):
        """Do the work."""
        while True:
            for data in generator():
                lead_colour = self.redisman.get_colour()
                tail_colour = scale_colour(lead_colour, 0.1)

                lead = populate_indeces(data["lead"], self.hat)
                tail = populate_indeces(data["tail"], self.hat)

                self.hat.colour_indeces(tail, tail_colour, auto_show=False)
                self.hat.colour_indeces(lead, lead_colour, auto_show=False)

                self.hat.show()


def populate_indeces(data, hat):
    """Populate some indeces."""
    indeces = []
    for pair in data:
        for pixel in hat:
            if close_enough(pixel["x"], pair[0]) and close_enough(pixel["z"], pair[1]):
                indeces.append(pixel["index"])

    return indeces


def generator():
    """Iterator."""
    for angle in range(0, 360, 10):
        yield {"lead": line(angle, 10), "tail": line(angle - 10, 10)}


def line(angle, resolution=100):
    """A line for an angle as a series of pairs of points."""
    res = resolution - 1
    line = []

    for i in range(res):
        factor = i / res
        line.append((cos(radians(angle)) * factor, sin(radians(angle)) * factor))

    line.append((cos(radians(angle)), sin(radians(angle))))

    return line


# https://stackoverflow.com/a/328337
def point_on_line(point, line):
    """Is a point on (or near enough) a line."""
    a, b = line
    a_x, a_y = a
    b_x, b_y = b
    c_x, c_y = point

    return (
        (b_x - a_x) * (c_y - a_y) == (c_x - a_x) * (b_y - a_y)
        and abs(cmp(a_x, c_x) + cmp(b_x, c_x)) <= 1
        and abs(cmp(a_y, c_y) + cmp(b_y, c_y)) <= 1
    )


def cmp(a, b):
    return (a > b) - (a < b)
