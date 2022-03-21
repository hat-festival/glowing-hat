from random import random

from lib.tools import hue_to_rgb


class RandomRoller:
    """Generate random colours.."""

    def __init__(self):
        """Construct."""
        self.name = "Random"

    @property
    def next(self):
        """Return the next colour."""
        return hue_to_rgb(random())
