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
        self.throbbers = []
        for _ in range(len(self.hat)):
            self.throbbers.append(Throbber(self.data["steps"]))

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            hue = self.custodian.get("hue")
            for pixel in self.hat.pixels:
                pixel["hue"] = hue
                pixel["value"] = self.throbbers[pixel["index"]].next()

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
