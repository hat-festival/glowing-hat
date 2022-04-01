class Larsen(list):
    """Larsen pre-renderer."""

    def __init__(self, length=100):
        """Construct."""
        self.length = length

    def populate(self):
        """Add data to self."""
        self.append([1])
        self.append([1, 0.5])
