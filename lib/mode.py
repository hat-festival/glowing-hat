import pickle
from pathlib import Path

from lib.axis_manager import AxisManager
from lib.conf import conf


class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat, custodian):
        """Construct."""
        self.hat = hat
        self.name = type(self).__name__.lower()
        self.custodian = custodian
        self.conf = conf
        self.data = self.conf.get("modes").get(self.name)
        self.prefs = self.data.get("prefs")
        self.manager = AxisManager()
        self.frame_sets = self.load_frame_sets()
        self.axis = self.custodian.get("axis")

    def get_colour(self):
        """Retrieve the colour from Redis."""
        return self.custodian.get("colour")

    def from_list(self, lights):
        """Illuminate our hat from a list of RGBs."""
        self.hat.illuminate(list(lights)[: len(self.hat)])

    def from_sort(self, sort_key):
        """Set the hat ordering from a sort_key."""
        self.hat.pixels = self.manager.get_sort(sort_key)

    def sort_hat(self, axis):
        """Sort the hat."""
        self.hat.sort(axis)

    def load_frame_sets(self):
        """Load the frame data."""
        data = None
        try:
            data = pickle.loads(Path("renders", f"{self.name}.pickle").read_bytes())  # noqa: S301
        except FileNotFoundError:
            try:  # noqa: SIM105
                data = pickle.loads(  # noqa: S301
                    Path(
                        "renders",
                        f"{self.__class__.__bases__[0].__name__.lower()}.pickle",
                    ).read_bytes()
                )
            except FileNotFoundError:
                pass

        return data
