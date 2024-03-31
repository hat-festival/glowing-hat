from lib.sorters.axis_manager import AxisManager
from lib.sorters.sorts_generator import SortsGenerator


class Circle:
    """Spin in a circle."""

    def __init__(self, *axes):
        """Construct."""
        self.manager = AxisManager()
        self.rotator = SortsGenerator(*axes)
        self.rotator.make_circle()

    def next(self):
        """Set the hat to the next entry and rotate the deque."""
        return self.manager.get_sort(self.rotator.next)
