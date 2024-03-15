from random import randint, random

from lib.mode import Mode
from lib.tools import scale_colour


class Sweeper(Mode):
    """Sweeper mode."""

    def reconfigure(self):
        """Configure ourself."""
        self.jump = self.data["jump"]
        self.frames = self.frame_sets["y-b"]
        self.blip_index = None

    def colour(self, clr, factor):
        """Get the colour."""
        return scale_colour(clr, factor)

    def run(self):
        """Do the work."""
        self.reconfigure()

        while True:
            count = 0
            if random() > self.data["blip-move-threshold"]:  # noqa: S311
                self.blip_index = None

            for frame in self.frames:
                if count % self.jump == 0:
                    self.illuminate(frame, [0, 255, 0])

                count += 1  # noqa: SIM113

            if not self.blip_index:
                self.blip_index = randint(0, 99)  # noqa: S311

    def illuminate(self, frame, clr):
        """Light the hat."""
        lights = [self.colour(clr, x[1]) for x in frame]
        if self.blip_index:
            lights[self.blip_index] = self.colour(
                [255, 0, 0], frame[self.blip_index][1]
            )
        self.from_list(lights)
