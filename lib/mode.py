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
        self.conf = conf
        self.custodian = Custodian()

        self.invert = self.custodian.get("invert")
        self.axis = self.custodian.get("axis")

    def get_colour(self):
        """Retrieve the colour from Redis."""
        return self.custodian.get("colour")

    @property
    def frame_sets(self):
        """Load the frame data."""
        return pickle.loads(Path("renders", f"{self.name}.pickle").read_bytes())
