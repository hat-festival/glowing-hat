from random import random

from glowing_hat.conf import conf


class RandomHueSource:
    """Generate spaced-out random hues."""

    def __init__(self):
        """Construct."""
        self.conf = conf
        self.current_hue = self.next_hue = random()  # noqa: S311

    def hue(self):
        """Get a hue."""
        while (
            abs(self.current_hue - self.next_hue) < self.conf["random-hue"]["distance"]
        ):
            self.next_hue = random()  # noqa: S311

        self.current_hue = self.next_hue

        return self.current_hue
