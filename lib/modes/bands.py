from collections import deque

from lib.conf import conf
from lib.mode import Mode
from lib.tools import colour_set_to_colour_list


class Bands(Mode):
    """Bands of colour."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.hat.sort(key=lambda w: w[self.axis])

        self.jump = self.conf["modes"]["bands"]["jump"]
        if self.invert:
            self.jump = 0 - self.jump

        self.width = self.conf["modes"]["bands"]["width"]

    def run(self):
        """Do the stuff."""
        bands = deque(
            colour_set_to_colour_list(
                conf["colour-sets"][self.custodian.get("colour-set")], self.width
            )
        )

        self.hat.off()
        while True:
            for i, _ in enumerate(self.hat):
                self.hat.light_one(self.hat[i]["index"], bands[i], auto_show=False)
            self.hat.show()
            bands.rotate(self.jump)
