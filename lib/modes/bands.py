from collections import deque

from lib.mode import Mode


class Bands(Mode):
    """Bands of colour."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        direction = "up"
        if self.invert:
            direction = "down"

        frames_key = f"{self.axis}_{direction}"

        frames = self.frame_sets[frames_key]

        self.data = deque(frames)

    def run(self):
        """Do the stuff."""
        self.hat.off()

        while True:
            colour = self.get_colour()
            for index, lights in enumerate(self.data):
                if index % self.conf["modes"][self.name]["steps"] == 0:
                    self.hat.colour_indeces(
                        list(map(lambda x: x["index"], lights)), colour
                    )
