from lib.redis_manager import RedisManager


class ZWave:
    """Simple wave mode."""

    def __init__(self, hat, steps=50):
        """Construct."""
        self.name = "Z-Wave"
        self.hat = hat
        self.steps = steps
        self.redis_man = RedisManager()

    def run(self):
        """Do stuff."""
        self.hat.off()
        while True:
            colour = self.redis_man.fetch_colour()
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
