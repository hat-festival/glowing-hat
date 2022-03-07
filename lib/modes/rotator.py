from collections import deque
from pathlib import Path

import yaml

from lib.mode import Mode
from lib.tools import scale_colour


class Rotator(Mode):
    """Rotator mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat, "rotator")

        frames = yaml.safe_load(
            Path("renders/rotator.yaml").read_text(encoding="UTF-8")
        )

        self.data = deque(frames)
        self.tail_data = deque(frames)

        self.tail_data.rotate(36)

    def run(self):
        """Do the work."""
        self.hat.off()
        while True:
            for index, lights in enumerate(self.data):
                if index % 6 == 0:
                    colour = self.redisman.get_colour()
                    tail_colour = scale_colour(colour, 0.1)
                    self.hat.colour_indeces(
                        self.tail_data[index], tail_colour, auto_show=False
                    )
                    self.hat.colour_indeces(lights, colour, auto_show=False)

                    self.hat.show()
