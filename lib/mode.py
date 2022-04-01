import pickle
from pathlib import Path

from lib.conf import conf
from lib.custodian import Custodian


class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat):
        """Construct."""
        self.hat = hat
        self.name = type(self).__name__.lower()
        self.custodian = Custodian()
        self.conf = conf
        self.data = self.conf["modes"][self.name]

        self.invert = self.custodian.get("invert")
        self.axis = self.custodian.get("axis")

    def set_preferred_axis(self):
        """Rotate to preferred axis for this mode."""
        if "preferred-axis" in self.data:
            self.custodian.rotate_until(self.data["preferred-axis"], "axis")
            self.axis = self.custodian.get("axis")

    def sort_hat(self):
        """Sort the hat."""
        self.hat.sort(key=lambda w: w[self.axis])

    def get_colour(self):
        """Retrieve the colour from Redis."""
        return self.custodian.get("colour")

    @property
    def frame_sets(self):
        """Load the frame data."""
        return pickle.loads(Path("renders", f"{self.name}.pickle").read_bytes())
