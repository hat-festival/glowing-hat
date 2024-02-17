import pickle
from collections import deque
from pathlib import Path
from random import randint

from lib.mode import Mode
from lib.tools import scale_colour

CURVES = pickle.loads(Path("renders", "pulsator.pickle").read_bytes())  # noqa: S301


class Pulsator(Mode):
    """A huge pulsating brain."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)

        self.throbbers = []
        for _ in range(self.hat.length):
            self.throbbers.append(Throbber())

    def reconfigure(self):
        """Reconfig some stuff."""
        # self.custodian.set("axis", "none")

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        while True:
            colour = self.get_colour()
            self.hat.illuminate(
                list(  # noqa: C417
                    map(
                        lambda throbber: scale_colour(colour, throbber.next()),
                        self.throbbers,
                    )
                )
            )


class Throbber:
    """Cos renderer."""

    def __init__(self):  # pylint: disable=W0231
        """Construct."""
        self.values = deque()

    def next(self):
        """Get the next value."""
        if len(self.values) == 0:
            key = randint(16, 255)  # noqa: S311
            self.values = deque(CURVES[key])

        value = self.values.popleft()

        return value  # noqa: RET504
