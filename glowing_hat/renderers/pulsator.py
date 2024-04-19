import pickle
from math import cos, pi
from pathlib import Path


class Pulsator(dict):
    """Pre-render cos-curved coefficients."""

    def __init__(self, limit=256):  # pylint: disable=W0231
        """Construct."""
        self.limit = limit

    def render(self):
        """Create the data."""
        for i in range(2, self.limit):
            self[i] = populate(i)

        Path("renders/pulsator.pickle").write_bytes(pickle.dumps(self))


def populate(steps):
    """Create a curve."""
    result = []
    accumulator = -1
    interval = (1 / steps) * 2

    while accumulator < 1:
        actual = cos(accumulator * pi)
        offset = actual + 1
        normalised = offset / 2
        rounded = round(normalised, 3)
        result.append(rounded)
        accumulator += interval

    return result
