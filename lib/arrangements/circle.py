from lib.axis_manager import AxisManager
from lib.sorts_generator import SortsGenerator


class Circle:
    """Spin in a circle."""

    def __init__(self, hat, *axes):
        """Construct."""
        self.manager = AxisManager()
        self.hat = hat
        self.rotator = SortsGenerator(*axes)
        self.rotator.make_circle()

# TODO: this should return indeces only
    def next(self):
        """Set the hat to the next entry and rotate the deque."""
        return tuple(x["index"] for x in self.manager.get_sort(self.rotator.next))
        # self.hat.pixels = self.manager.get_sort(self.rotator.next)
