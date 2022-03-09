from lib.mode import Mode


class Wave(Mode):
    """Simple wave mode."""

    def __init__(self, hat):
        """Construct."""
        self.name = "wave"
        super().__init__(hat, self.name)
        self.steps = self.conf["modes"][self.name]["steps"]

    def run(self):
        """Do stuff."""
        self.hat.off()

        while True:
            colour = self.get_colour()

            rng = range(self.steps)
            if self.invert:
                rng = range(self.steps, 0, -1)

            for i in rng:
                positives = list(
                    filter(
                        lambda w: w.positive(self.axis)
                        and w.less_than(self.axis, i / self.steps),
                        self.hat,
                    )
                )
                negatives = list(
                    filter(
                        lambda w: w.negative(self.axis)
                        and w.greater_than(self.axis, 0 - (i / self.steps)),
                        self.hat,
                    )
                )

                indeces = list(map(lambda x: x["index"], positives + negatives))
                self.hat.colour_indeces(indeces, colour)
