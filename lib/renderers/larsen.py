import pickle
from collections import deque
from math import cos, pi
from pathlib import Path


class Larsen(list):
    """Larsen pre-renderer."""

    def __init__(self, length=100):  # pylint: disable=W0231
        """Construct."""
        self.length = length

    def render(self):
        """Populate and save."""
        self.populate()
        Path("renders/larsen.pickle").write_bytes(pickle.dumps(self))

    def populate(self):
        """Add data to self."""
        middle = deque(middle_member(self.length))
        for _ in range(self.length):
            middle.append(0.0)
            middle.appendleft(0.0)

        for _ in range(2 * self.length - 1):
            middle.rotate(-1)
            self.append(list(middle)[0 : self.length])


def middle_member(length):
    """Generate the most-populated member."""
    member = []
    for i in range_finder(length):
        member.append(round(cos(i * pi) + 1, 3))  # noqa: PERF401

    return member


def range_finder(length):
    """Generate a scaled range."""
    results = []
    for i in range(length):
        results.append((i / (length * 2)) + 0.5)  # noqa: PERF401

    return results
