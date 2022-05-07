from collections import deque

from lib.mode import Mode
from lib.tools import colour_set_to_colour_list


class Bands(Mode):
    """Bands of colour."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)
        self.jump = self.data["jump"]
        self.width = self.data["width"]

    def reconfigure(self):
        """Configure ourself."""
        if self.invert:
            self.jump = 0 - self.jump

        self.bands = deque(
            colour_set_to_colour_list(
                self.conf["colour-sets"][self.custodian.get("colour-set")], self.width
            )
        )
        self.hat.sort(self.axis)

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        while True:
            self.hat.illuminate(list(self.bands)[:100])
            self.bands.rotate(self.jump)
