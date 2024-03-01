from collections import deque

from lib.axis_manager import AxisManager
from lib.mode import Mode
from lib.sorts_generator import SortsGenarator
from lib.tools import hue_to_rgb


class Cuttlefish(Mode):
    """Ripples of colour."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)
        self.jump = self.data["jump"]
        self.steps = self.data["steps"]
        self.colours = deque()
        for i in range(self.steps):
            self.colours.append(hue_to_rgb(i / self.steps))

    def reconfigure(self):
        """Configure ourself."""
        if self.invert:
            self.jump = 0 - self.jump

        self.sort_hat()

        self.manager = AxisManager()

        self.rotator = SortsGenarator(("x", "z"))
        self.rotator.make_circle()
        self.hat.pixels = self.manager.get_sort(self.rotator.next)

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        count = 0
        while True:
            self.hat.illuminate(list(self.colours)[: self.hat.length])
            count += 1
            # TODO move these numbers out to conf
            if count == 1:
                self.hat.pixels = self.manager.get_sort(self.rotator.next)
                count = 0

            self.colours.rotate(self.jump)
