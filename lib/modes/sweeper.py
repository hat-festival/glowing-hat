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
                    clr = self.get_colour()
                    for index, factor in frame:
                        self.hat.light_one(
                            index,
                            self.colour(clr, factor),
                            auto_show=False
                            # index, hue_to_rgb(factor), auto_show=False
                        )

                    self.hat.show()

                count += 1
