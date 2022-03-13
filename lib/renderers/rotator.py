import pickle
from math import cos, radians, sin
from pathlib import Path

import numpy as np

from lib.pixel_hat import PixelHat


class Rotator:
    """Rotator renderer."""

    def __init__(self):
        """Construct."""
        self.hat = PixelHat(auto_centre=True)

    def render(self):
        """Create the data"""
        # name these for the axis around which they rotate?
        data = {}
        for pair in [("x", "y"), ("y", "z"), ("x", "z")]:
            data[f"{pair[0]}_{pair[1]}"] = make_frameset(self.hat, pair[0], pair[1])

        Path("renders/rotator.pickle").write_bytes(pickle.dumps(data))


def make_frameset(hat, axis_1, axis_2):
    """Create the frames."""
    data = []
    for line in generator():
        pixels = populate_indeces(line, hat, axis_1, axis_2)
        data.append(pixels)

    return data


def populate_indeces(data, hat, axis_1, axis_2):
    """Populate some indeces."""
    return list(
        map(
            lambda x: x["index"],
            filter(
                lambda pixel: point_on_line((pixel[axis_1], pixel[axis_2]), data), hat
            ),
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
