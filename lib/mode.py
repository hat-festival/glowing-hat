import pickle
from pathlib import Path

from lib.conf import conf


class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat, custodian):
        """Construct."""
        self.hat = hat
        self.name = type(self).__name__.lower()
        self.custodian = custodian
        self.conf = conf
        self.data = self.conf["modes"][self.name]
        self.prefs = self.data["prefs"]

        self.invert = self.custodian.get("invert")
        self.axis = self.custodian.get("axis")

    def reset(self):
        """Reset some things."""
        self.set_preferred_axis()
        self.set_preferred_invert()
        self.reset_colour_sources()

    def set_preferred_invert(self):
        """Rotate to preferred inversion for this mode."""
        if "invert" in self.prefs:
            self.custodian.set("invert", str(self.prefs["invert"]))
            self.invert = self.custodian.get("invert")

    def set_preferred_axis(self):
        """Rotate to preferred axis for this mode."""
        if "axis" in self.prefs:
            if self.prefs["axis"] == "none":
                self.custodian.set("axis", "none")

            else:
                self.custodian.set("axis", self.prefs["axis"])
                self.axis = self.custodian.get("axis")

    def reset_colour_sources(self):
        """Load acceptable colour-sources for this mode."""
        if "colour-sources" in self.prefs:
            self.custodian.reset_colour_sources(self.prefs["colour-sources"])

        else:
            self.custodian.reset_colour_sources(["none"])

        self.custodian.next("colour-source")

        if "colour-set" in self.prefs:
            self.custodian.set("colour-set", self.prefs["colour-set"])
            self.custodian.next("colour")

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
