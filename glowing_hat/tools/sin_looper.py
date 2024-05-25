from math import pi, sin


class SinLooper:
    """Sin-curve iterator."""

    def __init__(self, low=0, high=1, steps=10):
        """Construct."""
        self.low = low
        self.high = high
        self.steps = steps
        self.interval = 1.0 / (self.steps / 2)

        self.x = 0

    def __iter__(self):
        """Be an iterator."""
        return self

    def __next__(self):
        """Get `next`."""
        value = number_scaler(self.low, self.high, sin(self.x))
        self.x = (self.x + (self.interval * pi)) % (2 * pi)

        return value


def number_scaler(low, high, value):
    """Scale a number."""
    return (((value + 1) / 2) * (high - low)) + low
