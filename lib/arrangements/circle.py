from lib.sorters.axis_manager import AxisManager
from lib.sorters.sorts_generator import SortsGenerator


class Circle:
    """Spin in a circle."""

    def __init__(self, *axes, steps=1):
        """Construct."""
        self.manager = AxisManager()
        self.rotator = SortsGenerator(*axes)
        self.rotator.make_circle()
        self.steps = steps

    def next(self):
        """Set the hat to the next entry and rotate the deque."""
        sort = None
        for _ in range(self.steps):
            sort = self.rotator.next

        return self.manager.get_sort(sort)
