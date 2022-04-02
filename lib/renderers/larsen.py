import pickle
from collections import deque
from pathlib import Path


class Larsen(list):
    """Larsen pre-renderer."""

    # THIS NEEDS TO BE SCALABLE SOMEHOW
    # USE A SIN-CURVE RATHER THAN A STRAIGHT LINE?
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
    for i in range(length):
        member.append((length - i) / length)

    return member
