class SpaceSolver:
    """Do some trig."""

    def __init__(self, point, steps=1000):
        """Construct."""
        self.point = point
        self.steps = steps
        self.calc_increments()
        self.calc_states()

    def calc_increments(self):
        """Calculate the increments."""
        self.increments = tuple(0 - (c / self.steps) for c in self.point)

    def calc_states(self):
        """Calculate the states."""
        self.states = []
        for i in range(self.steps * 2 + 1):
            self.states.append(
                tuple(
                    map(
                        sum,
                        zip(
                            self.point,
                            [c * i for c in self.increments],
                            strict=False,
                        ),
                    )
                )
            )
