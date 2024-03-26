import pickle
from collections import deque
from operator import itemgetter
from pathlib import Path
from random import randint

from lib.mode import Mode

CURVES = pickle.loads(Path("renders", "pulsator.pickle").read_bytes())  # noqa: S301


class Pulsator(Mode):
    """A huge pulsating brain."""

    def configure(self):
        """Reconfig some stuff."""
        self.throbbers = [Throbber(self.data["steps"]) for _ in range(len(self.hat))]

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            # TODO: this should be some generic object that just gives the hue.
            # Or maybe the PixelList gets it
            hue = self.custodian.get("hue")
            self.hat.apply_hue(hue)
            self.hat.apply_values([throbber.next() for throbber in self.throbbers])

            self.hat.light_up()


class Throbber:
    """Cos renderer."""

    def __init__(self, minmax):
        """Construct."""
        self.values = deque()
        self.min, self.max = itemgetter("min", "max")(minmax)

    def next(self):
        """Get the next value."""
        if len(self.values) == 0:
            key = randint(self.min, self.max)  # noqa: S311
            self.values = deque(CURVES[key])

        value = self.values.popleft()

        return value  # noqa: RET504
