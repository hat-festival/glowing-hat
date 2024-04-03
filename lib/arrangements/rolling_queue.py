class RollingQueue(list):
    """A queue that rolls."""

    def __init__(self, length):
        """Construct."""
        self.length = length
        for _i in range(length):
            self.append(None)

    def push(self, item):
        """Push something onto ourself."""
        for i in range(self.length - 1):
            self[i] = self[i + 1]

        self[-1] = item
