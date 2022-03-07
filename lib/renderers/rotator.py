from math import cos, radians, sin
from pathlib import Path

import numpy as np
import yaml


class Rotator:
    """Rotator renderer."""

    def __init__(self, hat):
        """Construct."""
        self.hat = hat

    def render(self):
        """Do the work."""
        data = []
        for line in generator():
            pixels = populate_indeces(line, self.hat)
            data.append(pixels)

        Path("renders/rotator.yaml").write_text(yaml.dump(data), encoding="UTF-8")


def populate_indeces(data, hat):
    """Populate some indeces."""
    return list(
        map(
            lambda x: x["index"],
            filter(lambda pixel: point_on_line((pixel["x"], pixel["z"]), data), hat),
        )
    )


def generator():
    """Iterator."""
    for angle in range(0, 360, 1):
        yield line(angle)


def line(angle):
    """A line for an angle."""
    return [(0, 0), (cos(radians(angle)), sin(radians(angle)))]


# https://stackoverflow.com/a/52756183
def point_on_line(point, line):
    """Is a point on (or near enough) a line."""
    tolerance = 0.1
    this_end = np.array(line[0])
    that_end = np.array(line[1])
    our_point = np.array(point)
    distance = np.cross(that_end - this_end, our_point - this_end) / np.linalg.norm(
        that_end - this_end
    )

    return abs(distance) <= tolerance
