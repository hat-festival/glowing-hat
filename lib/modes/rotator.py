import pickle
from collections import deque
from pathlib import Path

from lib.mode import Mode
from lib.tools import remove_axis, scale_colour


class Rotator(Mode):
    """Rotator mode."""

    frame_sets = pickle.loads(Path("renders/rotator.pickle").read_bytes())

    def __init__(self, hat):
        """Construct."""
        self.name = "rotator"
        super().__init__(hat, self.name)

        frames_key = "_".join(remove_axis(self.axis))

        frames = Rotator.frame_sets[frames_key]

        if self.invert:
            frames = list(reversed(frames))

        self.data = deque(frames)
        self.tail_data = deque(frames)

        self.tail_data.rotate(self.conf["modes"][self.name]["offset"])

    def run(self):
        """Do the work."""
        self.hat.off()
        while True:
            for index, lights in enumerate(self.data):
                if index % self.conf["modes"][self.name]["steps"] == 0:
                    colour = self.get_colour()
                    tail_colour = scale_colour(colour, 0.1)
                    self.hat.colour_indeces(
                        self.tail_data[index], tail_colour, auto_show=False
                    )
                    self.hat.colour_indeces(lights, colour, auto_show=False)

                    self.hat.show()
