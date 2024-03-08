from random import random

from lib.conf import conf
from lib.tools import hue_to_rgb


class RandomColourSource:
    """Generate spaced-out random colours."""

    def __init__(self):
        """Construct."""
        self.conf = conf
        self.hue = self.next_hue = random()  # noqa: S311

    @property
    def colour(self):
        """Get a colour."""
        while (
            abs(self.hue - self.next_hue) < self.conf["random-colour"]["hue-distance"]
        ):
            self.next_hue = random()  # noqa: S311

        self.hue = self.next_hue

        return hue_to_rgb(self.hue)
