class FreeRoller:
    """Use the rotating wheel."""

    def __init__(self):
        """Construct."""
        self.name = "wheel"

    @property
    def next(self):
        """Return the next colour."""
        return "wheel"
