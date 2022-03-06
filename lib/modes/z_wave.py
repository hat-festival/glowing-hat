from lib.mode import Mode


class ZWave(Mode):
    """Simple wave mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat, "Z-Wave")
        self.steps = 20

    def run(self):
        """Do stuff."""
        self.hat.off()
        while True:
            colour = self.redisman.get_colour()
            for i in range(self.steps):
                positives = list(
                    filter(
                        lambda w: w.positive("z") and w.less_than("z", i / self.steps),
                        self.hat,
                    )
                )
                negatives = list(
                    filter(
                        lambda w: w.negative("z")
                        and w.greater_than("z", 0 - (i / self.steps)),
                        self.hat,
                    )
                )
                indeces = list(map(lambda x: x["index"], positives + negatives))
                self.hat.colour_indeces(indeces, colour)
