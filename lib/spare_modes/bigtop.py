from lib.modes.sweeper import Sweeper
from lib.tools import hue_to_rgb


class BigTop(Sweeper):
    """BigTop mode."""

    def colour(self, _, factor):
        """Get the colour."""
        return hue_to_rgb(factor)
