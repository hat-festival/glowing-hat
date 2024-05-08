import time


class TimeBasedHueSource:
    """Get a hue based on the time."""

    def __init__(self, seconds_per_rotation=2):
        """Construct."""
        self.seconds_per_rotation = seconds_per_rotation

    def hue(self):
        """Get a hue based on the time."""
        now = time.time()
        return (now % self.seconds_per_rotation) / self.seconds_per_rotation

    def inverse_hue(self):
        """Get the inverse hue."""
        return (self.hue() + 0.5) % 1
