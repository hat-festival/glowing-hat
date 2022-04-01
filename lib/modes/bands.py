from collections import deque

from lib.mode import Mode
from lib.tools import colour_set_to_colour_list


class Bands(Mode):
    """Bands of colour."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.jump = self.data["jump"]
        if self.invert:
            self.jump = 0 - self.jump

        self.width = self.data["width"]

        self.bands = deque(
            colour_set_to_colour_list(
                self.conf["colour-sets"][self.custodian.get("colour-set")], self.width
            )
        )

    def run(self):
        """Do the stuff."""
        self.sort_hat()

        while True:
            for i, _ in enumerate(self.hat):
                self.hat.light_one(self.hat[i]["index"], self.bands[i], auto_show=False)
            self.hat.show()
            self.bands.rotate(self.jump)
