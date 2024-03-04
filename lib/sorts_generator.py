from collections import deque

from lib.sort_key import SortKey


class SortsGenerator:
    """Generate some axis patterns."""

    def __init__(self, *axes, interval=0.1):
        """Construct."""
        self.interval = interval
        self.axes = axes

    @property
    def live_indeces(self):
        """Work out which axes are in play."""
        return ["xyz".index(axis) for axis in self.axes]

    @property
    def start_corner(self):
        """Work out the starting point."""
        point = []
        for char in "xyz":
            if char in self.axes:
                point.append(-1.0)
            else:
                point.append(0.0)

        return SortKey(point)

    # TODO let this take a radius for the 1.1x1.1 sort
    def make_circle(self, direction="forwards", altitude=None):
        """Get a set of keys to go round and round."""
        if direction == "backwards":
            self.axes = list(self.axes)
            self.axes.reverse()
            self.axes = tuple(self.axes)

        self.keys = [self.start_corner]
        operations = ["increment", "decrement"]

        if altitude:
            self.keys[-1][({0, 1, 2} - set(self.live_indeces)).pop()] = altitude

        for operation in operations:
            for index in self.live_indeces:
                for _ in range(-10, 10, int(self.interval * 10)):
                    next_item = self.keys[-1].clone()
                    getattr(next_item, operation)(index, self.interval)
                    self.keys.append(next_item)

        self.keys.pop()
        self.hoop = deque(self.as_keys)

    @property
    def as_tuples(self):
        """Our keys as tuples."""
        return [x.tuple for x in self.keys]

    @property
    def as_keys(self):
        """Our keys as Redis keys."""
        return [x.as_key for x in self.keys]

    @property
    def next(self):
        """Get the next entry and rotate the deque."""
        self.hoop.rotate()
        return self.hoop[0]
