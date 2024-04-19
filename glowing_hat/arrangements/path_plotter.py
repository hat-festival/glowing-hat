class PathPlotter:
    """Plot a path."""

    def __init__(self, weighting=0.9):
        """Construct."""
        self.axes = {"x": 1.0, "y": 1.0, "z": 1.0}

        self.current_axis = "x"
        self.current_increment = 0.1  # positive

        self.weighting = weighting
