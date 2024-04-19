class SortKey:
    """Wrapper around a tuple-ish."""

    def __init__(self, *values):
        """Construct."""
        if len(values) == 1:
            if values[0].__class__.__name__ in ["list", "tuple"]:
                self.values = list(values[0])
        else:
            self.values = list(values)

    @property
    def tuple(self):
        """Us as a tuple."""
        return tuple(self.values)

    @property
    def as_key(self):
        """As a Redis key."""
        return f"sorts:{self.tuple}"

    def clone(self):
        """Clone ourselves."""
        return SortKey(self.values)

    def __setitem__(self, index, value):
        """Support index assignment."""
        self.values[index] = value

    def __getitem__(self, index):
        """Support index retrieval."""
        return self.values[index]

    def increment(self, index, amount):
        """Increment ourself."""
        self.values[index] = round(self.values[index] + amount, 1)

    def decrement(self, index, amount):
        """Increment ourself."""
        self.values[index] = round(self.values[index] - amount, 1)
