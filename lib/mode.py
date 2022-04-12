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
        self.prefs = self.data["prefs"]

        self.invert = self.custodian.get("invert")

        self.axis = self.custodian.get("axis")
        if self.axis == "none":
            self.set_preferred_axis()

    def set_preferred_axis(self):
        """Rotate to preferred axis for this mode."""
        if "axis" in self.prefs:
            if self.prefs["axis"] == "none":
                self.custodian.set("axis", "none")

            else:
                self.custodian.rotate_until("axis", self.prefs["axis"])
                self.axis = self.custodian.get("axis")

    def reset_colour_sources(self):
        """Load acceptable colour-sources for this mode."""
        if "colour-sources" in self.prefs:
            self.custodian.reset_colour_sources(self.prefs["colour-sources"])

        else:
            self.custodian.reset_colour_sources(["none"])

        self.custodian.next("colour-source")

    def sort_hat(self):
        """Sort the hat."""
        self.hat.sort(self.axis)

    def get_colour(self):
        """Retrieve the colour from Redis."""
        return self.custodian.get("colour")

    @property
    def frame_sets(self):
        """Load the frame data."""
        return pickle.loads(Path("renders", f"{self.name}.pickle").read_bytes())
