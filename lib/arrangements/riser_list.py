from random import random


class RiserList:
    """Colour values for a fade with a weighting."""

    def __init__(self, hat_length):
        """Construct."""
        self.hat_length = hat_length
        self.populate()

    def populate(self):
        """Fill in the data."""
        self.data = []
        for i in range(self.hat_length):
            if random() > i / self.hat_length:  # noqa: S311
                self.data.append("primary")
            else:
                self.data.append("secondary")
