from lib.mode import Mode
from lib.tools import scale_colour


class Sweeper(Mode):
    """Sweeper mode."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)
        self.jump = self.data["jump"]

    def reconfigure(self):
        """Configure ourself."""
        self.frames = self.frame_sets[f"{self.axis}-f"]
        if self.invert:
            self.frames = self.frame_sets[f"{self.axis}-b"]

    def colour(self, clr, factor):
        """Get the colour."""
        return scale_colour(clr, factor)

    def run(self):
        """Do the work."""
        self.reconfigure()

        while True:
            count = 0

            for frame in self.frames:
                if count % self.jump == 0:
                    self.illuminate(frame, self.get_colour())

                count += 1

    def illuminate(self, frame, clr):
        """Light the hat."""
        self.hat.illuminate(list(map(lambda x: self.colour(clr, x[1]), frame)))
