class SetRoller:
    """Roll some colours."""

    def __init__(self, name, colours):
        """Construct."""

        self.name = name
        self.colours = colours
        self.rgbs = list(self.colours.values())
        self.length = len(self.rgbs)
        self.index = 0

    @property
    def next(self):
        """Return the next colour."""
        colour = self.rgbs[self.index]
        self.index = (self.index + 1) % self.length

        return colour
